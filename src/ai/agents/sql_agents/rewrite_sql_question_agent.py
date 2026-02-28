#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/28 11:14
@Author  : tianshiyang
@File    : rewrite_sql_question_agent.py
"""
from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable, RunnableLambda

from ai import chat_qianwen_llm


def get_rewrite_question_agent_chain() -> RunnableSerializable[Any, str]:
    """获取重写查询问题的chain"""
    prompt = ChatPromptTemplate.from_template("""
        你是查询改写助手。
        将用户问题改写为完整查询：
        - 补全时间语义
        - 消除代词
        - 不生成SQL
        历史:
        {history}
        问题:
        {question}
    """)

    chain = {
            "history": RunnableLambda(func=lambda x: x["history"]),
            "question": RunnableLambda(func=lambda x: x["question"]),
            } | prompt | chat_qianwen_llm | StrOutputParser()
    return chain