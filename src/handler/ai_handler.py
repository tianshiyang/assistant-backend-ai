#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 18:20
@Author  : tianshiyang
@File    : ai_handler.py
"""
from flask_jwt_extended import jwt_required, get_jwt_identity

from schema.ai_schema import AIChatSchema


@jwt_required()
def ai_chat_handler():
    req = AIChatSchema()
    """与AI聊天对话"""
    user_id = get_jwt_identity()
    pass