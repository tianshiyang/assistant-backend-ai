#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/24 21:57
@Author  : tianshiyang
@File    : dataset_search_agent.py
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool

from ai import chat_qianwen_llm
from service.milvus_database_service import get_retriever_with_scores

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

dataset_search_prompt = PromptTemplate(
    template=DATASET_SEARCH_RAG_PROMPT,
    input_variables=["retrieved_context", "question"],
)

def get_dataset_search_result(question: str, dataset_id: str):
    """
    :param question: 用户提问的问题
    :param dataset_id: 关联的知识库 id
    :return: 知识库检索出来的结果，list of (Document, score)
    """
    return get_retriever_with_scores(
        query=question,
        min_score=0.8,
        expr=f"dataset_id=='{dataset_id}'",
    )


def _format_retrieved_docs(results):
    """把检索结果格式化为 RAG 上下文字符串。"""
    if not results:
        return "（未检索到相关文档）"

    search_result = "\n\n".join(
        f"[{i + 1}] {doc.page_content}"
        for i, doc in enumerate(results)
    )

    return search_result

def _build_rag_context(params: dict) -> str:
    """从链输入 {question, dataset_id} 调用检索并格式化为上下文。"""
    question = params["question"]
    dataset_id = params["dataset_id"]
    results = get_dataset_search_result(question=question, dataset_id=dataset_id)
    return _format_retrieved_docs(results)


@tool
def dataset_search_agent_tool(dataset_id: str, question: str):
    """
    获取知识库检索结果的Agent，当你需要进行知识库检索的时候，你可以调用此工具
    :param dataset_id: 知识库id
    :param question: 用户提问的问题
    :return: 大语言模型返回的知识库问题的回答
    """
    chain = (
            {
                "retrieved_context": RunnableLambda(_build_rag_context),
                "question": RunnableLambda(lambda inp: inp["question"]),
            }
            | dataset_search_prompt
            | chat_qianwen_llm
            | StrOutputParser()
    )
    # 链输入格式: {"question": "用户问题", "dataset_id": "知识库 id"}
    # 会先用 question + dataset_id 做知识库检索，再把检索结果与 question 一起交给 RAG 提示与 LLM
    return chain.invoke({
        "question": question,
        "dataset_id": dataset_id,
    })

if __name__ == "__main__":
    out = dataset_search_agent_tool.stream({
        "question": "电影《羞羞的铁拳》什么时候上映的",
        # "question": "今日上证50收盘多少点",
        "dataset_id": "ce949e61-4e52-4aeb-a97c-8aa77dea0f0f",
    }, stream_mode="messages")
    for doc in out:
        print(doc)