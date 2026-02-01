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
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from ai import chat_qianwen_llm
from config.db_config import db
from entities.ai import GENERATED_CONVERSATION_TITLE_PROMPT, GENERATED_USER_MAYBE_QUESTION_PROMPT
from entities.chat_response_entity import ChatResponseType, ChatResponseEntity
from entities.redis_entity import REDIS_CHAT_GENERATED_KEY
from model.conversation import Conversation
from model.message import Message
from pkg.exception import FailException
from schema.ai_schema import AIChatSchema, ConversationMessagesSchema, ConversationDeleteSchema, \
    ConversationUpdateSchema, ConversationMaybeQuestionSchema
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
                        yield f"event:message\ndata: {json.dumps(chunk, ensure_ascii=False)}\n\n"
                    
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
                    message_id="",
                    conversation_id=conversation_id,
                    tool_call=None
                )
                yield f"event:message\ndata: {json.dumps(message, ensure_ascii=False)}\n\n"
                last_ts = time.time()
    except Exception as e:
        # 如果发生异常，发送错误消息并退出
        error_message = ChatResponseEntity(
            updated_time=time.time(),
            content=f"流式响应错误: {str(e)}",
            type=ChatResponseType.ERROR,
            message_id="",
            conversation_id=conversation_id,
            tool_call=None
        )
        yield f"event:message\ndata: {json.dumps(error_message, ensure_ascii=False)}\n\n"
    finally:
        redis_stream.delete(redis_key)


def ai_create_conversation_service(user_id: str) -> Conversation:
    """创建新会话"""
    conversation = Conversation(
        name="新会话",
        user_id=user_id,
    ).create()
    return conversation

def ai_chat_service(req: AIChatSchema, user_id: str, conversation_id: str, is_new_chat: str):
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
        is_new_chat=is_new_chat
    )

def ai_chat_get_conversation_messages_service(req: ConversationMessagesSchema, user_id: str) -> list[Message]:
    """获取所有聊天内容"""
    return db.session.query(Message).filter(
        Message.conversation_id == req.conversation_id.data,
        Message.user_id == user_id
    ).order_by(
        Message.created_at.asc()
    ).all()

def ai_conversation_get_all_service(user_id: str) -> list[Conversation]:
    """获取所有会话"""
    return db.session.query(Conversation).filter(
        Conversation.user_id == user_id
    ).order_by(
        Conversation.created_at.desc()
    ).all()

def ai_conversation_delete_service(req: ConversationDeleteSchema, user_id: str) -> Conversation:
    """删除会话"""
    conversation = db.session.query(Conversation).filter(
        Conversation.id == req.conversation_id.data,
        Conversation.user_id == user_id
    ).first()

    if conversation is None:
        raise FailException("会话不存在")

    # 删除会话下的所有消息
    db.session.query(Message).filter(
        Message.conversation_id == conversation.id,
        Message.user_id == user_id
    ).delete()
    # 删除会话
    conversation.delete()
    return conversation

def get_conversation_detail_service(conversation_id: str, user_id: str) -> Conversation:
    """获取会话详情"""
    conversation = db.session.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()
    if conversation is None:
        raise FailException("会话不存在")
    return conversation

def update_conversation_title_service(conversation_id, user_id: str, name: str) -> Conversation:
    """更新会话主题信息"""
    conversation = get_conversation_detail_service(conversation_id=conversation_id, user_id=user_id)
    conversation.update(
        name=name
    )
    return conversation

def get_message_detail_service(message_id: str, user_id: str) -> Message:
    """获取会话详情"""
    message = db.session.query(Message).filter(
        Message.id == message_id,
        Message.user_id == user_id
    ).first()
    if message is None:
        raise FailException("会话不存在")
    return message


def ai_conversation_update_service(req: ConversationUpdateSchema, user_id: str) -> Conversation:
    """根据用户问题与 AI 回复生成并更新会话主题"""
    message = get_message_detail_service(message_id=req.message_id.data, user_id=user_id)

    system_prompt = GENERATED_CONVERSATION_TITLE_PROMPT.format(
        user_question=message.question,
        ai_answer=message.answer,
    )
    agent = create_agent(
        model=chat_qianwen_llm,
        system_prompt=system_prompt,
    )
    result = agent.invoke({
        "messages": [HumanMessage(content="请帮我生成本次回话的主题")],
    })
    conversation = update_conversation_title_service(
        conversation_id=message.conversation_id,
        user_id=user_id,
        name=result['messages'][-1].content
    )
    return conversation

def ai_conversation_maybe_question_service(req: ConversationMaybeQuestionSchema, user_id: str) -> list[str]:
    """生成用户可能询问的问题"""
    message = get_message_detail_service(message_id=req.message_id.data, user_id=user_id)
    system_prompt = GENERATED_USER_MAYBE_QUESTION_PROMPT.format(
        user_question=message.question,
        ai_answer=message.answer,
    )
    agent = create_agent(
        model=chat_qianwen_llm,
        system_prompt=system_prompt,
    )
    result = agent.invoke({
        "messages": [HumanMessage(content="请帮我生成用户可能询问的问题")],
    })
    question = result['messages'][-1].content.split("\n")
    return question