#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/28 11:15
@Author  : tianshiyang
@File    : base_sql_agent_service.py
"""
import json
import os
import re
import time
from typing import AsyncIterator, Literal

from flask import current_app
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage, ToolMessage

from ai import chat_qianwen_llm
from ai.service import BaseAgentService
from entities.chat_response_entity import SQLAgentResponseEntity, SQLManageResponseType
from entities.redis_entity import REDIS_TEXT_TO_SQL_KEY, REDIS_TEXT_STOP_TEXT_TO_SQL
from service.ai_service import get_message_detail_service
from service.message_service import create_message_service
from utils import build_mysql_uri, get_module_logger

# 获取日志记录器
logger = get_module_logger(__name__)


class BaseSQLAgentService(BaseAgentService):
    """基础SQLAgent"""
    def __init__(self, conversation_id: str, question: str, user_id: str) -> None:
        self.conversation_id = str(conversation_id)
        self.db_uri = os.getenv("POSTGRES_SHOT_MEMORY_URI")
        self.config = self.get_config(conversation_id=self.conversation_id)
        self.db = self.get_database_db()
        self.tools = self.get_sql_database_tools()
        self.sql_description = self.get_tables_description()

        self.raw_user_question = question # 用户原始的问题
        self.user_id = user_id
        self._message = None # message对象
        self._redis_client = current_app.redis_stream
        self.stop_stream_redis_conversation_key = REDIS_TEXT_STOP_TEXT_TO_SQL.format(conversation_id=self.conversation_id) # 停止text2Sql输出内容
        self._ai_chunks = [] # 存储每次返回给前端的数据，并存储到message中，作为历史记录
        self._ai_full_answer = "" # AI返回的完整的答案
        self._token_dict = None # 消耗token的情况

    def init_message(self, is_new_chat: bool, chat_type: Literal['chat', 'interaction'], message_id: str):
        """初始化message对象，先创建一个message消息"""
        if chat_type == 'interaction':
            # 人机交互的节点，直接返回message对象即可
            self._message = get_message_detail_service(message_id, user_id=self.user_id)
        if chat_type == 'chat':
            # 普通聊天节点，正常新增message
            self._create_message()
            if is_new_chat:
                self._send_chunk_to_redis(SQLAgentResponseEntity(
                    updated_time=time.time(),
                    content=str(self.conversation_id),
                    type=SQLManageResponseType.CREATE_CONVERSATION,
                    message_id=str(self._message.id),
                    conversation_id=str(self.conversation_id),
                ))

    def _create_message(self):
        """创建一个一条消息"""
        self._message = create_message_service(
            conversation_id=self.conversation_id,
            user_id=self.user_id,
            question=self.raw_user_question,
            messages="[]",
            answer="",
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
        )

    def _update_messages(self, chat_type: Literal['chat', 'interaction']):
        """保存聊天内容到message表中"""
        if chat_type == 'chat':
            self._message.update(
                question=self.raw_user_question,
                messages=json.dumps(self._ai_chunks),
                answer=self._ai_full_answer,
                input_tokens=self._token_dict.get("input_tokens") if self._token_dict else 0,
                output_tokens=self._token_dict.get("output_tokens") if self._token_dict else 0,
                total_tokens=self._token_dict.get("total_tokens") if self._token_dict else 0,
            )
        elif chat_type == 'interaction':
            cur_message = self._message.to_dict().get("messages", [])
            cur_message.extend(self._ai_chunks)
            cur_answer = self._message.to_dict().get("answer", [])

            logger.info(f"cur_message: {cur_message}")
            self._message.update(
                messages=json.dumps(cur_message),
                answer=cur_answer + self._ai_full_answer,
                input_tokens=self._token_dict.get("input_tokens") if self._token_dict else 0,
                output_tokens=self._token_dict.get("output_tokens") if self._token_dict else 0,
                total_tokens=self._token_dict.get("total_tokens") if self._token_dict else 0,
            )

    def _send_chunk_to_redis(self, payload: SQLAgentResponseEntity):
        """发送消息到redis中"""
        if payload["type"] != SQLManageResponseType.CREATE_CONVERSATION:
            # 创建回话不存入历史消息
            self._ai_chunks.append(payload)
        redis_key = REDIS_TEXT_TO_SQL_KEY.format(conversation_id=self.conversation_id)
        self._redis_client.rpush(redis_key, json.dumps(payload, ensure_ascii=False))

    def get_sql_database_tools(self):
        """加载数据库"""
        toolkit = SQLDatabaseToolkit(db=self.db, llm=chat_qianwen_llm)
        tools = toolkit.get_tools()
        return tools

    def get_tables_description(self) -> str:
        """获取mysql表格的描述信息"""
        db_schema_tool = None
        db_list_tool = None
        for tool in self.tools:
            if tool.name == "sql_db_schema":
                db_schema_tool = tool
        if not db_schema_tool and not db_list_tool:
            return "未找到任何表内容"
        return db_schema_tool.invoke(",".join(self.db.get_usable_table_names()))

    def _save_use_tokens(self, usage_metadata):
        """打印最终统计信息"""
        self._token_dict = {
            "input_tokens": usage_metadata.get('input_tokens'),
            "output_tokens": usage_metadata.get('output_tokens'),
            "total_tokens": usage_metadata.get('total_tokens'),
        }
        # 保存token用量
        self._send_chunk_to_redis(SQLAgentResponseEntity(
            updated_time=time.time(),
            content=self._token_dict,
            type=SQLManageResponseType.SAVE_TOKEN,
            message_id=str(self._message.id),
            conversation_id=str(self.conversation_id),
        ))

    def _stop_text_to_sql_chat(self):
        if self._redis_client.get(self.stop_stream_redis_conversation_key) == SQLManageResponseType.STOP.value:
            # 终止会话
            self._send_chunk_to_redis(SQLAgentResponseEntity(
                content="会话已终止",
                type=SQLManageResponseType.STOP,
                message_id=str(self._message.id),
                conversation_id=str(self.conversation_id),
                updated_time=time.time(),
            ))
            self._redis_client.delete(self.stop_stream_redis_conversation_key)
            return True
        return False

    @staticmethod
    def _extract_json_content(text: str) -> str:
        """从 AI 回复中提取 JSON，去除模型可能添加的前缀/后缀文字"""
        text = text.strip()
        # 去掉 markdown 代码块包裹
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        text = text.strip()

        # 尝试找到最外层的 { ... } 并验证是合法 JSON
        first_brace = text.find('{')
        if first_brace != -1:
            last_brace = text.rfind('}')
            if last_brace > first_brace:
                candidate = text[first_brace:last_brace + 1]
                try:
                    json.loads(candidate)
                    return candidate
                except json.JSONDecodeError:
                    pass

        # 提取失败，按原文兜底包装为 text 类型
        return json.dumps({"type": "text", "content": text}, ensure_ascii=False)

    def _handle_manage_chunks_process(self, chunk):
        """处理普通的message信息"""
        answer_tokens = None
        last_message = chunk['messages'][-1]
        logger.info("当前last_message: %s", last_message.pretty_print)
        if isinstance(last_message, ToolMessage):
            # 工具调用结果
            self._send_chunk_to_redis(SQLAgentResponseEntity(
                updated_time=time.time(),
                content=last_message.content,
                type=SQLManageResponseType.TOOL_RESULT,
                message_id=str(self._message.id),
                conversation_id=str(self.conversation_id),
            ))
        elif isinstance(last_message, AIMessage):
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                self._send_chunk_to_redis(SQLAgentResponseEntity(
                    updated_time=time.time(),
                    content=last_message.tool_calls[0]['name'],
                    type=SQLManageResponseType.TOOL_CALL,
                    message_id=str(self._message.id),
                    conversation_id=str(self.conversation_id),
                ))
                self._send_chunk_to_redis(SQLAgentResponseEntity(
                    updated_time=time.time(),
                    content=last_message.tool_calls[0]['args'],
                    type=SQLManageResponseType.TOOL_PARAMS,
                    message_id=str(self._message.id),
                    conversation_id=str(self.conversation_id),
                ))
            elif hasattr(last_message, "content") and last_message.content:
                cleaned = self._extract_json_content(last_message.content)
                self._send_chunk_to_redis(SQLAgentResponseEntity(
                    updated_time=time.time(),
                    content=cleaned,
                    type=SQLManageResponseType.GENERATE,
                    message_id=str(self._message.id),
                    conversation_id=str(self.conversation_id),
                ))
                self._ai_full_answer = cleaned
            if hasattr(last_message, "usage_metadata") and last_message.usage_metadata:
                answer_tokens = last_message.usage_metadata
                logger.info(f"answer_tokens信息：{answer_tokens}")
        return answer_tokens

    def _handle_interrupt_process(self, interrupt):
        """处理中断节点"""
        logger.info(f"interrupt: {interrupt}")
        for interrupt_chunk in interrupt:
            self._send_chunk_to_redis(SQLAgentResponseEntity(
                updated_time=time.time(),
                content=interrupt_chunk.value.get("action_requests"),
                conversation_id=str(self.conversation_id),
                message_id=str(self._message.id),
                type=SQLManageResponseType.INTERACTION,
            ))



    async def _handle_manage_chunks(self, chunks: AsyncIterator, seen_msg_count: int = 0):
        """处理agent的返回结果
        :param chunks: agent 的流式输出
        :param seen_msg_count: 已处理过的消息数量（用于 resume 时跳过旧状态重放）
        """
        is_stopped = False
        is_interrupted = False
        _final_answer_tokens = None
        async for chunk in chunks:
            # 判断是否停止
            is_stopped = self._stop_text_to_sql_chat()
            if is_stopped or is_interrupted:
                break
            if '__interrupt__' in chunk:
                # 处理中断类型的消息
                self._handle_interrupt_process(interrupt=chunk["__interrupt__"])
                is_interrupted = True
                break
            elif "messages" in chunk:
                current_count = len(chunk['messages'])
                if current_count <= seen_msg_count:
                    continue
                seen_msg_count = current_count
                # 处理普通消息
                _final_answer_tokens = self._handle_manage_chunks_process(chunk)

        # # 存储token消耗
        if _final_answer_tokens and not is_interrupted:
            self._save_use_tokens(_final_answer_tokens)

        if not is_stopped and not is_interrupted:
            self._save_finished_message()


    def _save_finished_message(self):
        """发送完成事件"""
        self._send_chunk_to_redis(SQLAgentResponseEntity(
            updated_time=time.time(),
            content="",
            type=SQLManageResponseType.DONE,
            message_id=str(self._message.id),
            conversation_id=str(self.conversation_id),
        ))

    @staticmethod
    def get_database_db():
        """获取数据库对象"""
        return SQLDatabase.from_uri(build_mysql_uri())