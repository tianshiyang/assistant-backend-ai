#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 18:20
@Author  : tianshiyang
@File    : ai_handler.py
"""
from flask import Response, stream_with_context, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from pkg.response import validate_error_json, success_json, success_message
from schema.ai_schema import AIChatSchema, ConversationMessagesSchema, ConversationDeleteSchema, \
    ConversationUpdateSchema, ConversationMaybeQuestionSchema, ConversationStopSchema, ManageAiChatSchema, \
    StopManageAiChatSchema, GetConversationListAllSchema, InteractionManageAiChatSchema, ContinueManageAIChatSchema, \
    CreateConversationSchema
from service.ai_service import ai_chat_service, ai_create_conversation_service, event_stream_service, \
    ai_chat_get_conversation_messages_service, ai_conversation_get_all_service, ai_conversation_delete_service, \
    ai_conversation_update_service, ai_conversation_maybe_question_service, ai_chat_stop_service, \
    manage_ai_chat_service, sql_manage_event_stream_service, stop_manage_ai_chat_service, interaction_ai_chat_service
from utils import get_module_logger

# 使用统一的日志记录器
logger = get_module_logger(__name__)

@jwt_required()
def create_conversation_handler():
    req = CreateConversationSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    question = req.question.data
    conversation_type = req.conversation_type.data
    user_id = get_jwt_identity()
    conversation = ai_create_conversation_service(
        user_id=user_id,
        conversation_type=conversation_type,
        chat_name=question
    )
    return success_json(conversation.to_dict())

@jwt_required()
def ai_chat_handler():
    req = AIChatSchema()
    """与AI聊天对话"""
    user_id = get_jwt_identity()
    conversation_id = req.conversation_id.data

    ai_chat_service(
        req=req,
        user_id=user_id,
        conversation_id=conversation_id,
    )
    return Response(
        stream_with_context(event_stream_service(conversation_id=conversation_id)),
        mimetype="text/event-stream; charset=utf-8"
    )

@jwt_required()
def ai_chat_stop_handler():
    req = ConversationStopSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    user_id = get_jwt_identity()
    ai_chat_stop_service(req=req, user_id=user_id)
    return success_message("停止成功")

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

@jwt_required()
def ai_conversation_get_all_handler():
    """获取所有会话列表"""
    req = GetConversationListAllSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    user_id = get_jwt_identity()
    resp = ai_conversation_get_all_service(user_id=user_id, req=req)
    result = []
    for message in resp:
        result.append(message.to_dict())
    return success_json(result)

@jwt_required()
def ai_conversation_delete_handler():
    """删除会话"""
    req = ConversationDeleteSchema()
    user_id = get_jwt_identity()
    ai_conversation_delete_service(req=req, user_id=user_id)
    return success_message("删除成功！")

@jwt_required()
def ai_conversation_update_handler():
    """总结会话主题"""
    req = ConversationUpdateSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    user_id = get_jwt_identity()
    res = ai_conversation_update_service(req=req, user_id=user_id)
    return success_json(res.to_dict())

@jwt_required()
def ai_conversation_maybe_question_handler():
    """生成可能询问的问题"""
    req = ConversationMaybeQuestionSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    user_id = get_jwt_identity()
    res = ai_conversation_maybe_question_service(req=req, user_id=user_id)
    return success_json({
        "question_list": res
    })

@jwt_required()
def manage_ai_chat_handler():
    """后台AI对话"""
    req = ManageAiChatSchema()

    if not req.validate():
        return validate_error_json(req.errors)

    user_id = get_jwt_identity()
    conversation_id = req.conversation_id.data



    manage_ai_chat_service(
        conversation_id=conversation_id,
        question=req.question.data,
        user_id=user_id,
    )

    return Response(
        stream_with_context(sql_manage_event_stream_service(conversation_id=conversation_id)),
        mimetype="text/event-stream; charset=utf-8"
    )

@jwt_required()
def stop_manage_ai_chat_handler():
    """停止后台Text2SQL的AI对话"""
    req = StopManageAiChatSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    user_id = get_jwt_identity()
    stop_manage_ai_chat_service(req=req, user_id=user_id)
    return success_message("停止会话成功")

@jwt_required()
def interaction_ai_chat_handler():
    req = InteractionManageAiChatSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    user_id = get_jwt_identity()
    interaction_ai_chat_service(req=req, user_id=user_id)
    return success_message("人机对话重启成功")

@jwt_required()
def continue_interaction_ai_chat_handler():
    req = ContinueManageAIChatSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    conversation_id = req.conversation_id.data
    return Response(
        stream_with_context(sql_manage_event_stream_service(conversation_id=conversation_id)),
        mimetype="text/event-stream; charset=utf-8"
    )
