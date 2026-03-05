#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 18:15
@Author  : tianshiyang
@File    : ai_router.py
"""
from flask import Blueprint

from handler.ai_handler import ai_chat_handler, ai_chat_get_conversation_messages_handler, \
    ai_conversation_get_all_handler, ai_conversation_delete_handler, ai_conversation_update_handler, \
    ai_conversation_maybe_question_handler, ai_chat_stop_handler, manage_ai_chat_handler, \
    stop_manage_ai_chat_handler, interaction_ai_chat_handler, continue_interaction_ai_chat_handler, \
    create_conversation_handler

ai_blueprint = Blueprint("chat", __name__, url_prefix="")

# 创建回话
ai_blueprint.add_url_rule("/api/ai/conversation/create", methods=["POST"], view_func=create_conversation_handler)

# 对话
ai_blueprint.add_url_rule("/api/ai/chat", methods=["POST"], view_func=ai_chat_handler)

# 中断对话
ai_blueprint.add_url_rule("/api/ai/chat/stop", methods=["POST"], view_func=ai_chat_stop_handler)

# 获取所有会话
ai_blueprint.add_url_rule("/api/ai/conversation/all", view_func=ai_conversation_get_all_handler)

# 删除会话
ai_blueprint.add_url_rule("/api/ai/conversation/delete", methods=["POST"], view_func=ai_conversation_delete_handler)

# 获取会话下的所有内容
ai_blueprint.add_url_rule("/api/ai/conversation/messages", view_func=ai_chat_get_conversation_messages_handler)

# 获取和更新会话主题
ai_blueprint.add_url_rule("/api/ai/conversation/update_conversation_title", view_func=ai_conversation_update_handler)

# 生成本地聊天的用户可能问出的问题
ai_blueprint.add_url_rule("/api/ai/conversation/user_maybe_question", methods=["POST"], view_func=ai_conversation_maybe_question_handler)

"""后台AI接口"""
# 后台AI对话
ai_blueprint.add_url_rule("/api/manage/ai/chat", methods=["POST"], view_func=manage_ai_chat_handler)

# 停止后台AI对话
ai_blueprint.add_url_rule("/api/manage/ai/chat/stop", methods=["POST"], view_func=stop_manage_ai_chat_handler)

# 中断节点的继续对话
ai_blueprint.add_url_rule("/api/manage/ai/chat/interaction", methods=["POST"], view_func=interaction_ai_chat_handler)

# 获取后续的输出内容
ai_blueprint.add_url_rule("/api/manage/ai/chat/interaction/continue", methods=["POST"], view_func=continue_interaction_ai_chat_handler)