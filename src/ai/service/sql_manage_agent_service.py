#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/27 16:51
@Author  : tianshiyang
@File    : sql_manage_agent_service.py
"""
import asyncio
import time

import dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from ai import chat_qianwen_llm
from ai.agents.sql_agents import GeneratorSqlAgent, get_rewrite_question_agent_chain, BaseSQLAgentService
from ai.prompts.prompts import SUMMARIZATION_MIDDLEWARE_PROMPT, VISUALIZATION_AGENT_PROMPT
from entities.chat_response_entity import SQLAgentResponseEntity, ChatResponseType, SQLManageResponseType

dotenv.load_dotenv()

@tool
def generator_sql_tool(conversation_id: str, question: str, user_id: str) -> str:
    """
    用途：生成用户问题对应的sql语句，当你需要获取要执行的sql语句的时候，你可以使用此方法
    :param conversation_id: 当前会话的id
    :param question: 重写过后的用户的问题
    :param user_id: 向AI对话的用户id
    :return: 生成的sql语句
    """
    sql_agent_result = GeneratorSqlAgent(
        conversation_id=conversation_id,
        question=question,
        user_id=user_id,
    ).build_sql_agent()
    return sql_agent_result

class SQLManageAgentService(BaseSQLAgentService):
    """后台管理系统的agent"""
    def __init__(self, conversation_id: str, question: str, is_new_chat: bool, user_id: str) -> None:
        super().__init__(conversation_id=conversation_id, question=question, user_id=user_id)

        # 初始化message信息
        self.init_message(is_new_chat=is_new_chat)

    async def build_sql_manage_agent(self):

        async with AsyncPostgresSaver.from_conn_string(self.db_uri) as checkpointer:
            # 更改用户查询的问题
            self._send_chunk_to_redis(SQLAgentResponseEntity( # 开始重写问题
                content="",
                type=SQLManageResponseType.REWRITE_QUESTION_START,
                updated_time=time.time(),
                message_id=str(self._message.id),
                conversation_id=str(self.conversation_id)
            ))
            rewrite_question_chain = get_rewrite_question_agent_chain()
            checkpoint = await checkpointer.aget(self.config)
            channel_values = (checkpoint or {}).get("channel_values") or {}
            messages = channel_values.get("messages") or []
            recent = messages[-6:]
            # prompt 需要字符串，把消息列表格式化为 "role: content"
            history_str = "\n".join(
                f"{getattr(m, 'type', 'message')}: {getattr(m, 'content', '') or ''}"
                for m in recent
            ) or "（无历史）"
            rewrite_question = rewrite_question_chain.invoke({
                "question": self.raw_user_question,
                "history": history_str,
            })

            self._send_chunk_to_redis(SQLAgentResponseEntity( # 重写问题完成
                content=rewrite_question,
                type=SQLManageResponseType.REWRITE_QUESTION_END,
                updated_time=time.time(),
                message_id=str(self._message.id),
                conversation_id=str(self.conversation_id)
            ))

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
                stream_mode="values",
                config=self.config
            )

            await self._handle_manage_chunks(chunks)
            # 完成后保存会话消息
            self._update_messages()

if __name__ == "__main__":
    async def run_agent():
        # execute_agent = GeneratorSqlAgentService(question="我现在有哪些商品", conversation_id="conversation_123")
        # execute_agent.build_sql_agent()
        execute_agent = SQLManageAgentService(question="我现在有哪些商品", conversation_id="conversation_123", is_new_chat=False, user_id="tianshiyang")
        await execute_agent.build_sql_manage_agent()

    asyncio.run(run_agent())
