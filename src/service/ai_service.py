#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 21:25
@Author  : tianshiyang
@File    : ai_service.py
"""
from model.conversation import Conversation
from schema.ai_schema import AIChatSchema
from task import run_ai_chat_task

def ai_create_conversation_service(user_id: str) -> Conversation:
    conversation = Conversation(
        name="新会话",
        user_id=user_id,
    ).create()
    return conversation

def ai_chat_service(req: AIChatSchema, user_id: str):
    """AI聊天"""
    skills = req.skills.data
    question = req.question.data
    dataset_ids = req.dataset_ids.data
    conversation_id = req.conversation_id.data

    run_ai_chat_task.delay(
        user_id=user_id,
        conversation_id=conversation_id,
        question=question,
        dataset_ids=dataset_ids,
        skills=skills
    )
