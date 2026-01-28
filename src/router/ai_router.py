#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 18:15
@Author  : tianshiyang
@File    : ai_router.py
"""
from flask import Blueprint

from handler.ai_handler import ai_chat_handler, ai_create_conversation_handler

ai_blueprint = Blueprint("chat", __name__, url_prefix="")

# 对话
ai_blueprint.add_url_rule("/api/ai/chat", methods=["POST"], view_func=ai_chat_handler)