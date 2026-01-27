#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 18:20
@Author  : tianshiyang
@File    : ai_handler.py
"""
from flask_jwt_extended import jwt_required, get_jwt_identity

from pkg.response import success_message
from schema.ai_schema import AIChatSchema
from service.ai_service import ai_chat_service


@jwt_required()
def ai_chat_handler():
    req = AIChatSchema()
    """与AI聊天对话"""
    user_id = get_jwt_identity()
    ai_chat_service(req, user_id)
    return success_message("成功")