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
from langchain_core.prompts import PromptTemplate, SystemMessagePromptTemplate
from langgraph.prebuilt import ToolRuntime
from pydantic import BaseModel
from ai import chat_qianwen_llm
from service.milvus_database_service import get_retriever_with_scores
from utils import get_module_logger

logger = get_module_logger(__name__)

class Context(BaseModel):
    dataset_ids: list[str]

# 知识库检索RAG提示词
DATASET_SEARCH_RAG_PROMPT = """
    你是一个基于检索增强生成（RAG）系统的问答助手。你的回答必须严格依据提供的知识库文档上下文。请遵循以下规则：
        1. 仅使用当前提供的上下文信息回答问题，不得依赖外部知识、常识或推测。
        2. 如果上下文中包含与问题直接相关且明确的信息，请用简洁清晰的语言作答，并尽量引用原文关键内容。
        3. 如果上下文中没有提及该问题相关内容，或信息模糊、不完整、无法确定答案，请明确回复：“根据现有知识库文档，未找到与该问题相关的内容。”
        4. 不得编造、推断、假设或补充上下文未提供的信息。
    现在，请根据上述规则和以下提供的上下文回答用户的问题：
    【上下文开始】
    {retrieved_context}
    【上下文结束】
    用户问题：{question}
"""

dataset_search_prompt = SystemMessagePromptTemplate.from_template(
    template=DATASET_SEARCH_RAG_PROMPT,
    input_variables=["retrieved_context", "question"],
)


@tool
def get_dataset_search_result(
    question: str,
    runtime: ToolRuntime[Context],
) -> str:
    """
    根据用户提问的问题，获取知识库的检索结果。当你需要进行知识库检索时调用此工具。
    :param question: 用户提问的问题
    :return: 检索到的知识库内容摘要，供后续回答使用
    """
    raws = get_retriever_with_scores(
        query=question,
        k=20,
        min_score=0.8,
        dense_weight=0.7,  # 语义相似度权重（对于这类问题可以调高）
        sparse_weight=0.3,  # 关键词匹配权重
        final_k=5,  # 最终返回前5个最相关的结果
        expr=f"dataset_id in {runtime.context.dataset_ids}",
    )
    logger.info(f"检索到的文档raws:{raws}, 用户的问题：{question}, expr: dataset_id in {runtime.context.dataset_ids}")
    if not raws:
        return "（未检索到相关文档）"
    return "\n\n".join([raw.page_content for raw in raws])


@tool
def dataset_search_agent_tool(question: str, runtime: ToolRuntime):
    """
    获取知识库检索结果的 Agent，当你需要进行知识库检索时调用此工具。
    :param question: 用户提问的问题
    :return: 大语言模型基于知识库检索后的回答
    """
    # 从父 agent 的 context 注入 dataset_ids，保证与请求一致、不可被 LLM 篡改
    dataset_ids = runtime.context.dataset_ids
    if not dataset_ids:
        return "未指定要检索的知识库，请先选择知识库。"

    agent = create_agent(
        model=chat_qianwen_llm,
        tools=[get_dataset_search_result],
        context_schema=Context,
        name="dataset_search_agent",
        system_prompt=DATASET_SEARCH_RAG_PROMPT,
    )
    try:
        agent_result = agent.invoke(
            {"messages": [HumanMessage(content=question)]},
            context=Context(dataset_ids=dataset_ids),
        )
        return agent_result["messages"][-1].content
    except Exception as e:
        return f"知识库检索出错，出错原因{e}"


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
