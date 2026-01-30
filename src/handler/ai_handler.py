#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 18:20
@Author  : tianshiyang
@File    : ai_handler.py
"""
from flask import Response, stream_with_context, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from pkg.response import validate_error_json, success_json
from schema.ai_schema import AIChatSchema, ConversationMessagesSchema
from service.ai_service import ai_chat_service, ai_create_conversation_service, event_stream_service, \
    ai_chat_get_conversation_messages_service


@jwt_required()
def ai_chat_handler():
    req = AIChatSchema()
    """与AI聊天对话"""
    user_id = get_jwt_identity()
    conversation_id = req.conversation_id.data
    if req.conversation_id.data is None:
        # 如果没传递conversation_id，则代表的是一个新的会话
        conversation_id = ai_create_conversation_service(user_id).id
    ai_chat_service(
        req=req,
        user_id=user_id,
        conversation_id=conversation_id,
    )
    return Response(
        stream_with_context(event_stream_service(conversation_id=conversation_id)),
        mimetype="text/event-stream"
    )

@jwt_required()
def ai_chat_get_conversation_messages_handler():
    req = ConversationMessagesSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    user_id = get_jwt_identity()
    resp = ai_chat_get_conversation_messages_service(req=req, user_id=user_id)
    result = []
    for message in resp:
        result.append(message.to_dict())
    return success_json(result)
