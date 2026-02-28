#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/27 16:50
@Author  : tianshiyang
@File    : base_agent_service.py
"""
from langchain_core.runnables import RunnableConfig


class BaseAgentService:
    @staticmethod
    def get_config(conversation_id: str) -> RunnableConfig:
        return RunnableConfig(
            configurable={
                "thread_id": conversation_id,
            }
        )