#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 21:59
@Author  : tianshiyang
@File    : agent_service.py
"""
import json
import os
import time
from typing import AsyncIterator, Any

from flask import current_app
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import HumanMessage, AnyMessage
from langchain_core.runnables import RunnableConfig

from ai import chat_qianwen_llm
from ai.agents import dataset_search_agent_tool
from ai.agents.web_search_agent import web_search_agent_tool
from entities.ai_entity import Skills
from ai.prompts.prompts import SUMMARIZATION_MIDDLEWARE_PROMPT, PARENT_AGENT_PROMPT
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from entities.chat_response_entity import ChatResponseEntity, ChatResponseType, AgentContextSchema
from entities.redis_entity import REDIS_CHAT_GENERATED_KEY
from model.message import Message
from service.message_service import create_message_service
from utils import get_module_logger

logger = get_module_logger(__name__)

tool_entity = {
    Skills.DATASET_RETRIEVER.value: dataset_search_agent_tool,  # 知识库检索Agent
    Skills.WEB_SEARCH.value: web_search_agent_tool  # web搜索agent
}


class AgentService:
    """AI Agent 服务类"""

    def __init__(
            self,
            question: str,
            user_id: str,
            conversation_id: str,
            dataset_ids: list[str],
            skills: list[Skills],
            is_new_chat: bool
    ):
        """
        初始化 AgentService

        Args:
            question: 用户问题
            user_id: 用户ID
            conversation_id: 会话ID
            dataset_ids: 数据集ID列表
            skills: 技能列表
            is_new_chat: 是否新会话
        """
        self.is_new_chat = is_new_chat
        self.user_id = user_id
        self.dataset_ids = dataset_ids
        self.question = question
        self.conversation_id = conversation_id
        self._tools = []
        self._message: Message | None = None  # 消息实例
        self._token_dict = {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
        }
        self._ai_full_answer = ""
        self._redis = current_app.redis_stream
        self._ai_chunks = []  # AI输出的内容
        self._build_tools(skills)

    def _build_tools(self, skills: list[Skills]) -> None:
        """构建工具列表"""
        for skill in skills:
            tool = tool_entity.get(skill)
            if tool:
                self._tools.append(tool)

    def _update_chunk_to_redis(self, payload: ChatResponseEntity) -> None:
        """更新流内容到redis中"""
        # 保存AI输出的内容
        self._ai_chunks.append(payload)

        redis_key = REDIS_CHAT_GENERATED_KEY.format(conversation_id=self.conversation_id)
        self._redis.rpush(redis_key, json.dumps(payload, ensure_ascii=False))

    async def _handle_stream_chunks(self, chunks: AsyncIterator[dict[str, Any] | Any]) -> None:
        """处理 async stream 流"""
        final_answer_tokens = None  # 最终答案阶段的 token 统计

        async for chunk in chunks:
            if isinstance(chunk, tuple) and len(chunk) == 2:
                message_chunk, metadata = chunk
                # 根据消息类型处理
                msg_type = message_chunk.__class__.__name__
                if msg_type == "AIMessageChunk":
                    if hasattr(message_chunk, "tool_calls") and message_chunk.tool_calls and message_chunk.tool_calls[0]['name']:
                        # 工具调用
                        self._update_chunk_to_redis(ChatResponseEntity(
                            updated_time=time.time(),
                            content="",
                            type=ChatResponseType.TOOL,
                            message_id=str(self._message.id),
                            conversation_id=self.conversation_id,
                            tool_call=message_chunk.tool_calls[0]['name']
                        ))
                    elif hasattr(message_chunk, 'content') and message_chunk.content:
                        # 保存AI输出内容
                        self._update_chunk_to_redis(ChatResponseEntity(
                            updated_time=time.time(),
                            content=message_chunk.content,
                            message_id=str(self._message.id),
                            type=ChatResponseType.GENERATE,
                            conversation_id=self.conversation_id,
                            tool_call=None
                        ))
                        self._ai_full_answer += message_chunk.content
                elif msg_type == "ToolMessage":
                    self._update_chunk_to_redis(ChatResponseEntity(
                        updated_time=time.time(),
                        content=message_chunk.content,
                        type=ChatResponseType.TOOL_RESULT,
                        message_id=str(self._message.id),
                        tool_call=None,
                        conversation_id=self.conversation_id
                    ))

                # 检查是否有 usage_metadata（token 统计）
                if hasattr(message_chunk, "usage_metadata") and message_chunk.usage_metadata:
                    final_answer_tokens = message_chunk.usage_metadata

        # 打印最终统计信息
        if final_answer_tokens:
            self._token_dict = {
                "input_tokens": final_answer_tokens.get('input_tokens'),
                "output_tokens": final_answer_tokens.get('output_tokens'),
                "total_tokens": final_answer_tokens.get('total_tokens'),
            }
            # 保存token用量
            self._update_chunk_to_redis(ChatResponseEntity(
                updated_time=time.time(),
                content=self._token_dict,
                type=ChatResponseType.SAVE_TOKEN,
                message_id=str(self._message.id),
                tool_call=None,
                conversation_id=self.conversation_id
            ))

        # 发送完成事件
        self._update_chunk_to_redis(ChatResponseEntity(
            updated_time=time.time(),
            content="",
            type=ChatResponseType.DONE,
            message_id=str(self._message.id),
            tool_call=None,
            conversation_id=self.conversation_id
        ))

    def _create_messages(self) -> Message:
        """创建一个一条消息"""
        self._message = create_message_service(
            conversation_id=self.conversation_id,
            user_id=self.user_id,
            question=self.question,
            messages="[]",
            answer="",
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
        )
        return self._message

    def _save_messages(self):
        """保存聊天内容到message表中"""
        self._message.update(
            question=self.question,
            messages=json.dumps(self._ai_chunks),
            answer=self._ai_full_answer,
            input_tokens=self._token_dict.get("input_tokens"),
            output_tokens=self._token_dict.get("output_tokens"),
            total_tokens=self._token_dict.get("total_tokens"),
        )

    def _handle_tool_callback(self, tool_callback_type: ChatResponseType, content: str) -> None:
        """处理工具内部的回调函数"""
        self._update_chunk_to_redis(
            ChatResponseEntity(
                updated_time=time.time(),
                content=content,
                type=tool_callback_type,
                message_id=str(self._message.id),
                tool_call=None,
                conversation_id=self.conversation_id
            )
        )

    async def build_agent(self) -> None:
        """构建智能体并执行异步流式响应"""
        # 创建一条消息，用于获取当前消息的message_id
        self._create_messages()

        if self.is_new_chat:
            logger.info("向redis中添加了一条创建会话的消息")
            # 如果是新会话，则保存conversation_id并返回给前端
            self._update_chunk_to_redis(ChatResponseEntity(
                updated_time=time.time(),
                content="",
                type=ChatResponseType.CREATE_CONVERSATION,
                tool_call=None,
                message_id=str(self._message.id),
                conversation_id=self.conversation_id
            ))

        db_uri = os.getenv("POSTGRES_SHOT_MEMORY_URI")

        try:
            async with AsyncPostgresSaver.from_conn_string(db_uri) as checkpointer:
                logger.error(f"可调用的工具：{self._tools}")
                # 创建 agent
                agent = create_agent(
                    model=chat_qianwen_llm,
                    tools=self._tools,
                    context_schema=AgentContextSchema,
                    middleware=[
                        SummarizationMiddleware(
                            model=chat_qianwen_llm,
                            trigger=[('tokens', 4000), ("messages", 100)],
                            summary_prompt=SUMMARIZATION_MIDDLEWARE_PROMPT
                        )
                    ],
                    system_prompt=PARENT_AGENT_PROMPT,
                    checkpointer=checkpointer,
                )

                # 执行异步流式响应
                chunks = agent.astream(
                    {
                        "messages": [HumanMessage(content=self.question)],
                    },
                    stream_mode="messages",
                    config=self.get_config(conversation_id=self.conversation_id),
                    context=AgentContextSchema(
                        dataset_ids=self.dataset_ids,
                        function_callable=self._handle_tool_callback
                    ),
                )
                # 处理 async stream 流
                await self._handle_stream_chunks(chunks=chunks)
                # 保存聊天内容到数据库中
                self._save_messages()

        except Exception as e:
            self._update_chunk_to_redis(ChatResponseEntity(
                updated_time=time.time(),
                content=f"生成失败，错误原因：{str(e)}",
                type=ChatResponseType.ERROR,
                message_id=str(self._message.id) if self._message else '',
                tool_call=None,
                conversation_id=self.conversation_id
            ))
            logger.error(f"Agent 处理出错，会话ID: {self.conversation_id}, 错误: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def get_config(conversation_id: str) -> RunnableConfig:
        return RunnableConfig(
            configurable={
                "thread_id": conversation_id,
            }
        )
