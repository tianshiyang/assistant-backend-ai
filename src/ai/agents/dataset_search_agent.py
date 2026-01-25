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


class Context(BaseModel):
    dataset_id: str

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
        min_score=0.8,
        expr=f"dataset_id=='{runtime.context.dataset_id}'",
    )
    if not raws:
        return "（未检索到相关文档）"
    return "\n\n".join([raw.page_content for raw in raws])


@tool
def dataset_search_agent_tool(question: str, dataset_id: str):
    """
    获取知识库检索结果的Agent，当你需要进行知识库检索的时候，你可以调用此工具
    :param dataset_id: 知识库id
    :param question: 用户提问的问题
    :return: 大语言模型返回的知识库问题的回答
    """

    agent = create_agent(
        model=chat_qianwen_llm,
        tools=[get_dataset_search_result],
        context_schema=Context,
        name="dataset_search_agent",
        system_prompt=DATASET_SEARCH_RAG_PROMPT,
    )
    return agent.stream(
        {
            "messages": [HumanMessage(question)],
        },
        context=Context(
            dataset_id=dataset_id,
        ),
        stream_mode = "messages",
    )

if __name__ == "__main__":
    results = dataset_search_agent_tool.invoke({
        "question": "电影《羞羞的铁拳》什么时候上映的",
        "dataset_id": "ce949e61-4e52-4aeb-a97c-8aa77dea0f0f",
    })
    # agent.stream() 返回的是迭代器，需要消费才能拿到每条消息
    for chunk in results:
        print(chunk)