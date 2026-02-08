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
    from service.agent_service import AgentService

    agent_service = AgentService(
        user_id=user_id,
        conversation_id=conversation_id,
        question=question,
        dataset_ids=dataset_ids,
        skills=skills,
        is_new_chat=is_new_chat
    )
    asyncio.run(agent_service.build_agent())