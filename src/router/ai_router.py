#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 18:15
@Author  : tianshiyang
@File    : ai_router.py
"""
from flask import Blueprint

from handler.ai_handler import ai_chat_handler, ai_chat_get_conversation_messages_handler, ai_conversation_get_all_handler, ai_conversation_delete_handler

ai_blueprint = Blueprint("chat", __name__, url_prefix="")

# 对话
ai_blueprint.add_url_rule("/api/ai/chat", methods=["POST"], view_func=ai_chat_handler)

# 获取所有会话
ai_blueprint.add_url_rule("/api/ai/conversation/all", view_func=ai_conversation_get_all_handler)

# 删除会话
ai_blueprint.add_url_rule("/api/ai/conversation/delete", methods=["POST"], view_func=ai_conversation_delete_handler)

# 获取会话下的所有内容
ai_blueprint.add_url_rule("/api/ai/conversation/messages", view_func=ai_chat_get_conversation_messages_handler)