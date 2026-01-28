#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/27 10:53
@Author  : tianshiyang
@File    : ai_task.py
"""
from celery import shared_task

from entities.ai import Skills
from service.agent_service import AgentService
from utils import get_module_logger

logger = get_module_logger(__name__)


@shared_task
def run_ai_chat_task(
        user_id: str,
        conversation_id: str,
        question: str,
        dataset_ids: list[str],
        skills: list[Skills],
        is_new_conversation: bool = False
):
    """执行 AI 聊天任务"""
    logger.info(f"开始执行AI生成任务，用户ID: {user_id}, 会话ID: {conversation_id}")
    
    # 使用上下文管理器确保资源正确释放（即使出错也会关闭连接）
    agent_service = AgentService(
        user_id=user_id,
        conversation_id=conversation_id,
        question=question,
        dataset_ids=dataset_ids,
        skills=skills,
        is_new_conversation=is_new_conversation
    )
    agent_service.build_agent()

    logger.info(f"AI生成任务完成，用户ID: {user_id}, 会话ID: {conversation_id}")