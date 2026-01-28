#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 21:25
@Author  : tianshiyang
@File    : ai_service.py
"""
import json
import time

from flask import current_app

from entities.chat_response_entity import ChatResponseType, ChatResponseEntity
from entities.redis_entity import REDIS_CHAT_GENERATED_KEY
from model.conversation import Conversation
from schema.ai_schema import AIChatSchema
from task import run_ai_chat_task
from typing import Generator

def event_stream_service(conversation_id: str) -> Generator:
    """
    事件流服务，用于 SSE (Server-Sent Events) 流式响应
    """
    # 在函数开始时获取 redis_stream 引用（此时还在应用上下文中）
    redis_stream = current_app.redis_stream
    redis_key = REDIS_CHAT_GENERATED_KEY.format(conversation_id=conversation_id)
    last_ts = 0
    last_index = 0
    should_exit = False  # 标志变量，控制外层循环退出
    
    try:
        while True:
            # 检查退出标志
            if should_exit:
                break
            
            # 使用之前获取的引用，而不是 current_app.redis_stream
            chunks = redis_stream.lrange(redis_key, last_index, -1)
            if chunks and len(chunks) > 0:
                for chunk_json in chunks:
                    chunk = json.loads(chunk_json)
                    if chunk['updated_time'] > last_ts:
                        last_ts = chunk['updated_time']
                        yield f"event:message\ndata: {json.dumps(chunk)}\n\n"
                    
                    # 检查是否完成或出错
                    if chunk["type"] in (ChatResponseType.DONE.value, ChatResponseType.ERROR.value):
                        # 设置退出标志
                        should_exit = True
                        break
                
                # 更新索引，避免重复处理
                if chunks:
                    last_index += len(chunks)
            elif time.time() - last_ts > 2:
                # 超时发送 ping 消息
                message = ChatResponseEntity(
                    updated_time=time.time(),
                    content="",
                    type=ChatResponseType.PING,
                    tool_call=None
                )
                yield f"event:message\ndata: {json.dumps(message)}\n\n"
                last_ts = time.time()
    except Exception as e:
        # 如果发生异常，发送错误消息并退出
        error_message = ChatResponseEntity(
            updated_time=time.time(),
            content=f"流式响应错误: {str(e)}",
            type=ChatResponseType.ERROR,
            tool_call=None
        )
        yield f"event:message\ndata: {json.dumps(error_message)}\n\n"
    finally:
        redis_stream.delete(redis_key)


def ai_create_conversation_service(user_id: str) -> Conversation:
    """创建新会话"""
    conversation = Conversation(
        name="新会话",
        user_id=user_id,
    ).create()
    return conversation

def ai_chat_service(req: AIChatSchema, user_id: str, conversation_id: str, is_new_conversation: bool):
    """AI聊天"""
    skills = req.skills.data
    question = req.question.data
    dataset_ids = req.dataset_ids.data

    run_ai_chat_task.delay(
        user_id=user_id,
        conversation_id=conversation_id,
        question=question,
        dataset_ids=dataset_ids,
        skills=skills,
        is_new_conversation=is_new_conversation,
    )
