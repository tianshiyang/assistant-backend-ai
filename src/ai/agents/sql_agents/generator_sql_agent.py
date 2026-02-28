#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/28 11:17
@Author  : tianshiyang
@File    : generator_sql_agent.py
"""
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from ai import chat_qianwen_llm
from ai.agents.sql_agents.base_sql_agent_service import BaseSQLAgentService
from ai.prompts.prompts import TEXT_2_SQL_PROMPT


class GeneratorSqlAgent(BaseSQLAgentService):
    """生成SQL语句的Agent"""
    def __init__(self, conversation_id: str, question: str) -> None:
        super().__init__(conversation_id=conversation_id)
        self.question = question

    def build_sql_agent(self):
        manage_agent = create_agent(
            model=chat_qianwen_llm,
            system_prompt=TEXT_2_SQL_PROMPT.format(
                question=self.question,
                schema=self.sql_description
            ),
            tools=self.tools,
        )
        chunk = manage_agent.invoke(
            {
                "messages": [HumanMessage(content=self.question)]
            },
        )
        return chunk["messages"][-1].content