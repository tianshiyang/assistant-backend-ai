#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/27 10:53
@Author  : tianshiyang
@File    : ai_task.py
"""
import asyncio

from celery import shared_task

from entities.ai_entity import Skills
from utils import get_module_logger

logger = get_module_logger(__name__)


@shared_task
def run_ai_chat_task(
        user_id: str,
        conversation_id: str,
        question: str,
        dataset_ids: list[str],
        skills: list[Skills],
        is_new_chat: bool
):
    """执行 AI 聊天任务"""
    from ai.service.agent_service import AgentService

    agent_service = AgentService(
        user_id=user_id,
        conversation_id=conversation_id,
        question=question,
        dataset_ids=dataset_ids,
        skills=skills,
        is_new_chat=is_new_chat
    )
    asyncio.run(agent_service.build_agent())

@shared_task
def run_manage_ai_chat_task(conversation_id, question: str, is_new_chat: bool, user_id: str, message_id: str = None):
    from ai.service.sql_manage_agent_service import SQLManageAgentService
    sql_agent_service = SQLManageAgentService(
        conversation_id=conversation_id,
        question=question,
        is_new_chat=is_new_chat,
        user_id=user_id,
        chat_type="chat",
        message_id=message_id
    )
    asyncio.run(sql_agent_service.build_sql_manage_agent())

@shared_task
def run_interaction_manage_ai_chat_task(conversation_id, resume: str, user_id: str, message_id: str):
    from ai.service.sql_manage_agent_service import SQLManageAgentService
    # 这里不再需要重新提问，因此 question 传空串，且 is_new_chat=False
    sql_agent_service = SQLManageAgentService(
        conversation_id=conversation_id,
        question="",
        is_new_chat=False,
        user_id=user_id,
        chat_type="interaction",
        message_id=message_id
    )
    asyncio.run(sql_agent_service.continue_sql_manage_agent(resume=resume))
