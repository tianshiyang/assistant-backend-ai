#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/24 21:57
@Author  : tianshiyang
@File    : dataset_search_agent.py
"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolRuntime
from ai import chat_qianwen_llm
from ai.prompts.prompts import DATASET_SEARCH_RAG_PROMPT
from entities.chat_response_entity import AgentContextSchema, ChatResponseType, SearchToolProcessDataSchema
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
) -> list[Document] | str:
    """
    从知识库中检索与用户问题相关的文档片段（RAG 检索步骤）。
    
    此工具会：
    1. 在指定的知识库（dataset_ids）中搜索与 question 语义相似的内容
    2. 返回最相关的文档片段（最多 5 段）
    3. 如果未找到相关内容，返回"（未检索到相关文档）"
    
    Args:
        question: 用户的问题，用于检索相关文档
        
    Returns:
        检索到的文档内容列表，或"（未检索到相关文档）"
    """
    dataset_ids = _dataset_ids_from_context(runtime.context)
    
    expr = _build_dataset_ids_expr(dataset_ids)
    raws = get_retriever_with_scores(
        query=question,
        k=20,
        min_score=0.3,
        dense_weight=0.7,
        sparse_weight=0.3,
        final_k=5,
        expr=expr,
    )
    logger.error(f"检索的问题：{question}, 检索的知识库id：{dataset_ids}, 检索到的结果：{raws}")
    if not raws:
        return "（未检索到相关文档）"
    return raws


@tool
def dataset_search_agent_tool(question: str, runtime: ToolRuntime[AgentContextSchema]):
    """
    知识库检索子 Agent：基于 RAG（检索增强生成）从指定知识库中检索相关内容并生成回答。
    
    此工具是一个子 Agent，内部执行流程：
    1. 从 context 中获取要检索的知识库 ID 列表（dataset_ids）
    2. 调用 get_dataset_search_result 工具在指定知识库中进行语义检索
    3. 基于检索到的文档片段生成回答（严格依据文档内容，不编造信息）
    4. 如果未找到相关内容，明确告知用户"根据现有知识库文档，未找到与该问题相关的内容"
    5. 返回格式化的结构化输出（SearchToolProcessDataSchema 格式）
    
    Args:
        question: 用户的问题，用于在知识库中检索相关内容
        runtime: ToolRuntime[AgentContextSchema]
        
    Returns:
        dict: Agent 执行结果，包含：
            - messages: 对话消息列表
            - structured_response (可选): 格式化的搜索结果（SearchToolProcessDataSchema 格式）
        
    注意：
        - 如果 context 中未指定 dataset_ids，将返回错误提示
        - 此工具会严格基于检索到的文档内容回答，不会添加文档中未出现的信息
    """
    dataset_ids = _dataset_ids_from_context(runtime.context)
    if not dataset_ids:
        return "未指定要检索的知识库，请先选择知识库。"

    agent = create_agent(
        model=chat_qianwen_llm,
        tools=[get_dataset_search_result],
        context_schema=AgentContextSchema,
        response_format=SearchToolProcessDataSchema,
        system_prompt=DATASET_SEARCH_RAG_PROMPT,
    )
    try:
        agent_result = agent.invoke(
            {"messages": [HumanMessage(content=question)]},
            context=AgentContextSchema(
                **runtime.context,
            ),
        )
        return agent_result['structured_response'].model_dump()
    except Exception as e:
        logger.error(f"知识库检索出错，出错原因：{str(e)}")
        return f"知识库检索出错，出错原因：{str(e)}"


# if __name__ == "__main__":
#     cur_agent = create_agent(
#         model=chat_qianwen_llm,
#         tools=[get_dataset_search_result],
#         response_format=SearchToolProcessDataSchema,
#         system_prompt="""你是一个基于检索增强生成（RAG）的问答助手。
#
# 工作流程：
# 1. 当你收到用户问题时，必须首先调用 get_dataset_search_result 工具进行知识库检索
# 2. 工具会返回检索到的相关文档片段（可能为空）
# 3. 你必须严格基于工具返回的文档内容回答问题
# 4. 完成回答后，必须使用结构化输出工具（根据 response_format 定义的格式）返回格式化的搜索结果
#
# 重要：回答完成后，必须调用结构化输出工具返回格式化的结果。"""
#     )
#
#     result = cur_agent.invoke({
#         "messages": [HumanMessage(content="羞羞的铁拳是哪年上映的")]
#     },
#         context=AgentContextSchema(
#             dataset_ids=["2fb02169-29f9-4ffc-91a4-49f7ef4eb39e"]
#         ),
#     )
#
#     print(result['structured_response'].model_dump())
