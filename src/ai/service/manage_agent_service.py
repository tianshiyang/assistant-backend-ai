#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/27 16:51
@Author  : tianshiyang
@File    : manage_agent_service.py
"""
import asyncio
from typing import AsyncIterator

import dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from ai import chat_qianwen_llm
from ai.agents.sql_agents import GeneratorSqlAgent, get_rewrite_question_agent_chain, BaseSQLAgentService
from ai.prompts.prompts import SUMMARIZATION_MIDDLEWARE_PROMPT, VISUALIZATION_AGENT_PROMPT

dotenv.load_dotenv()

@tool
def generator_sql_tool(conversation_id: str, question: str) -> str:
    """
    用途：生成用户问题对应的sql语句，当你需要获取要执行的sql语句的时候，你可以使用此方法
    :param conversation_id: 当前会话的id
    :param question: 重写过后的用户的问题
    :return: 生成的sql语句
    """
    sql_agent_result = GeneratorSqlAgent(conversation_id=conversation_id, question=question).build_sql_agent()
    return sql_agent_result

class ManageService(BaseSQLAgentService):
    """后台管理系统的agent"""
    def __init__(self, conversation_id: str, question: str) -> None:
        super().__init__(conversation_id=conversation_id)
        self.question = question

    async def _handle_manage_chunks(self, chunks: AsyncIterator):
        """处理agent的返回结果"""
        result = ""
        async for chunk in chunks:
            if isinstance(chunk, tuple) and len(chunk) == 2:
                message_chunk, metadata = chunk
                if isinstance(message_chunk, AIMessage):
                    result += message_chunk.content
            print(chunk)
        print(result)

    async def build_manage_agent(self):

        async with AsyncPostgresSaver.from_conn_string(self.db_uri) as checkpointer:
            # 更改用户查询的问题
            rewrite_question_chain = get_rewrite_question_agent_chain()
            channel_values = await checkpointer.aget(self.config)
            history = channel_values.get("channel_values").get("messages")[-6:]
            rewrite_question = rewrite_question_chain.invoke({
                "question": self.question,
                "history": history
            })

            # text_2_sql agent
            manage_agent = create_agent(
                model=chat_qianwen_llm,
                middleware=[
                    SummarizationMiddleware(
                        model=chat_qianwen_llm,
                        trigger=[('tokens', 4000), ("messages", 100)],
                        summary_prompt=SUMMARIZATION_MIDDLEWARE_PROMPT
                    )
                ],
                tools=[generator_sql_tool, *self.tools],
                system_prompt=VISUALIZATION_AGENT_PROMPT,
                checkpointer=checkpointer,
            )

            chunks = manage_agent.astream(
                {
                    "messages": [HumanMessage(content=rewrite_question)]
                },
                stream_mode="messages",
                config=self.config
            )

            await self._handle_manage_chunks(chunks)

if __name__ == "__main__":
    async def run_agent():
        # execute_agent = GeneratorSqlAgentService(question="我现在有哪些商品", conversation_id="conversation_123")
        # execute_agent.build_sql_agent()
        execute_agent = ManageService(question="我现在有哪些商品", conversation_id="conversation_123")
        await execute_agent.build_manage_agent()

    asyncio.run(run_agent())
