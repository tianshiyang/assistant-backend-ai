#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/24 21:57
@Author  : tianshiyang
@File    : dataset_search_agent.py
"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolRuntime
from pydantic import BaseModel
from ai import chat_qianwen_llm
from entities.ai import DATASET_SEARCH_RAG_PROMPT
from entities.chat_response_entity import AgentContextSchema, ChatResponseType
from service.milvus_database_service import get_retriever_with_scores
from utils import get_module_logger

logger = get_module_logger(__name__)


def _dataset_ids_from_context(context) -> list[str]:
    """从父/子 agent 的 context 中安全取出 dataset_ids"""
    if context is None:
        return []
    if isinstance(context, dict):
        return list(context.get("dataset_ids") or [])
    return list(getattr(context, "dataset_ids", []) or [])

def _function_callable_from_context(
    context: AgentContextSchema,
    response_content: str,
    response_type: ChatResponseType = ChatResponseType.TOOL_PROCESS, # 默认工具执行的过程数据
):
    """从父agent的context中取出_function_callable_from_context"""
    return context["function_callable"](response_type, response_content)


def _build_dataset_ids_expr(dataset_ids: list[str]) -> str:
    """构建 Milvus 过滤表达式：dataset_id in ["id1", "id2"]。"""
    if not dataset_ids:
        return ""
    ids_str = ", ".join(f'"{s}"' for s in dataset_ids)
    return f"dataset_id in [{ids_str}]"


@tool
def get_dataset_search_result(
    question: str,
    runtime: ToolRuntime[AgentContextSchema],
) -> str:
    """
    从知识库中检索与用户问题相关的文档片段（RAG 检索步骤）。
    
    此工具会：
    1. 在指定的知识库（dataset_ids）中搜索与 question 语义相似的内容
    2. 返回最相关的文档片段（最多 5 段）
    3. 如果未找到相关内容，返回"（未检索到相关文档）"
    
    Args:
        question: 用户的问题，用于检索相关文档
        
    Returns:
        检索到的文档内容（多个片段用双换行分隔），或"（未检索到相关文档）"
    """
    dataset_ids = _dataset_ids_from_context(runtime.context)
    if not dataset_ids:
        return "（未检索到相关文档：未指定知识库）"
    
    expr = _build_dataset_ids_expr(dataset_ids)
    raws = get_retriever_with_scores(
        query=question,
        k=20,
        min_score=0.8,
        dense_weight=0.7,
        sparse_weight=0.3,
        final_k=5,
        expr=expr,
    )
    logger.info(f"检索的问题：{question[:50]}\n检索的结果：{raws}")
    if not raws:
        _function_callable_from_context(
            context=runtime.context,
            response_type=ChatResponseType.TOOL_PROCESS,
            response_content="(未检索到相关文档)"
        )
        return "（未检索到相关文档）"

    dataset_context = "\n\n".join([raw.page_content for raw in raws])
    _function_callable_from_context(
        context=runtime.context,
        response_type=ChatResponseType.TOOL_PROCESS,
        response_content=dataset_context
    )
    return dataset_context


@tool
def dataset_search_agent_tool(question: str, runtime: ToolRuntime[AgentContextSchema]):
    """
    知识库检索 Agent：基于 RAG 检索知识库并生成回答。
    
    此工具内部会：
    1. 调用检索工具从知识库中查找相关内容
    2. 基于检索结果生成回答（严格依据文档内容）
    3. 如果未找到相关内容，明确告知用户
    
    Args:
        question: 用户的问题
        
    Returns:
        基于知识库检索结果的回答（如果未找到相关内容会明确说明）
    """
    dataset_ids = _dataset_ids_from_context(runtime.context)
    if not dataset_ids:
        return "未指定要检索的知识库，请先选择知识库。"

    agent = create_agent(
        model=chat_qianwen_llm,
        tools=[get_dataset_search_result],
        context_schema=AgentContextSchema,
        name="dataset_search_agent",
        system_prompt=DATASET_SEARCH_RAG_PROMPT,
    )
    try:
        agent_result = agent.invoke(
            {"messages": [HumanMessage(content=question)]},
            context=AgentContextSchema(
                **runtime.context,
            ),
        )
        # 取最后一条 AI 消息的 content
        if isinstance(agent_result, dict) and agent_result.get("messages"):
            last = agent_result["messages"][-1]
            content = getattr(last, "content", None) if hasattr(last, "content") else (last.get("content") if isinstance(last, dict) else None)
            if content:
                return str(content).strip()
        return str(agent_result).strip()
    except Exception as e:
        logger.exception("知识库检索 Agent 执行失败: %s", e)
        return f"知识库检索出错，出错原因：{str(e)}"


# if __name__ == "__main__":
#     chunks = dataset_search_agent_tool.invoke({
#         "question": "电影《羞羞的铁拳》什么时候上映的",
#         "dataset_ids": ["ce949e61-4e52-4aeb-a97c-8aa77dea0f0f"],
#     })
#     # agent.stream() 返回的是迭代器，需要消费才能拿到每条消息
#     current_step = None
#     current_node = None
#     full_content = ""
#
#     # Token 统计
#     final_answer_tokens = None  # 最终答案阶段的 token 统计
#     for chunk in chunks:
#         if isinstance(chunk, tuple) and len(chunk) == 2:
#             message_chunk, metadata = chunk
#             # 获取langgraph信息
#             step = metadata.get("langgraph_step", 'N/A')
#             node = metadata.get('langgraph_node', 'N/A')
#             if current_node != step and current_step != step:
#                 if current_step is not None:
#                     print()  # 换行
#                 print(f"\n【步骤 {step} - 节点: {node}】")
#                 current_step = step
#                 current_node = node
#
#             # 根据消息类型处理
#             msg_type = message_chunk.__class__.__name__
#             if msg_type == "AIMessageChunk":
#                 if hasattr(message_chunk, "tool_calls") and message_chunk.tool_calls:
#                     print(f"  → AI 决定调用工具: {message_chunk.tool_calls[0]['name']}")
#                     print(f"  → 工具参数: {message_chunk.tool_calls[0]['args']}")
#                 elif hasattr(message_chunk, 'content') and message_chunk.content:
#                     # 实时打印内容（打字机效果）
#                     print(message_chunk.content, end="", flush=True)
#                     full_content += message_chunk.content
#             elif msg_type == "ToolMessage":
#                 print(f"\n  → 工具执行结果: {message_chunk.content}")
#                 print(f"  → 工具名称: {message_chunk.name}")
#
#             # 检查是否有 usage_metadata（token 统计），最后一个chunk内容为'',并且有usage_metadata字段
#             if hasattr(message_chunk, "usage_metadata") and message_chunk.usage_metadata:
#                 usage = message_chunk.usage_metadata
#                 # 判断是工具调用阶段还是最终答案阶段
#                 finish_reason = message_chunk.response_metadata.get('finish_reason', '') if hasattr(message_chunk,
#                                                                                                     'response_metadata') else ''
#                 # 最终答案阶段的 token 统计
#                 final_answer_tokens = usage
#     print(
#         f"  → [最终答案阶段] Token 使用: 输入={final_answer_tokens.get('input_tokens')}, 输出={final_answer_tokens.get("output_tokens")}, 总计={final_answer_tokens.get('total_tokens')}")
#
