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
from service.ai_service import ai_chat_service, ai_create_conversation_service


@jwt_required()
def ai_chat_handler():
    req = AIChatSchema()
    """与AI聊天对话"""
    user_id = get_jwt_identity()
    conversation_id = req.conversation_id.data
    if req.conversation_id.data is None:
        # 新任务
        conversation_id = ai_create_conversation_service(user_id).id
    ai_chat_service(
        req=req,
        user_id=user_id,
        conversation_id=conversation_id,
        is_new_conversation = req.conversation_id.data is None,
    )
    return success_message("成功")