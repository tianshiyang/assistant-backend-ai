#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 18:23
@Author  : tianshiyang
@File    : ai_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Optional
from schema.schema import ListField, DictField


class GetConversationListAllSchema(FlaskForm):
    type = StringField("type", validators=[
        DataRequired(message="会话类型不能为空")
    ])

class AIChatSchema(FlaskForm):
    """聊天"""
    dataset_ids = ListField("dataset_ids", default=[])
    skills = ListField("skills", default=[])
    conversation_id = StringField("conversation_id", validators=[
        Optional()
    ])
    question = StringField("question", validators=[
        DataRequired("提问的问题不能为空")
    ])

class ConversationMessagesSchema(FlaskForm):
    """获取某个会话下的所有消息"""
    conversation_id = StringField("conversation_id", validators=[
        DataRequired("会话id必传")
    ])

class ConversationStopSchema(FlaskForm):
    """获取某个会话下的所有消息"""
    conversation_id = StringField("conversation_id", validators=[
        DataRequired("会话id必传")
    ])

class ConversationDeleteSchema(FlaskForm):
    """删除会话"""
    conversation_id = StringField("conversation_id", validators=[
        DataRequired("会话id必传")
    ])

class ConversationUpdateSchema(FlaskForm):
    """总结并更新会话主题"""
    message_id = StringField("message_id", validators=[
        DataRequired("会话id必传")
    ])

class ConversationMaybeQuestionSchema(FlaskForm):
    """生成用户可能询问的问题"""
    message_id = StringField("message_id", validators=[
        DataRequired("会话id必传")
    ])

class ManageAiChatSchema(FlaskForm):
    """AI对话-后台部分"""
    conversation_id = StringField("conversation_id", validators=[])
    message_id = StringField("message_id", validators=[])
    question = StringField("query", validators=[DataRequired("用户问题必传")])

class StopManageAiChatSchema(FlaskForm):
    """停止Text2SQL的AI对话"""
    conversation_id = StringField("conversation_id", validators=[
        DataRequired("会话ID必传")
    ])

class InteractionManageAiChatSchema(FlaskForm):
    """人机回话"""
    conversation_id = StringField("conversation_id", validators=[
        DataRequired("会话ID必传")
    ])
    # 人机交互时用于恢复执行的内容（如 approve/reject/edit 等决策或编辑后的内容）
    resume = DictField("resume", validators=[
        DataRequired("人机交互内容必传")
    ])
    message_id = StringField("message_id", validators=[DataRequired("会话id必传")])

class ContinueManageAIChatSchema(FlaskForm):
    """继续获取人机对话后的输出内容"""
    conversation_id = StringField("conversation_id", validators=[
        DataRequired("会话ID必传")
    ])

class CreateConversationSchema(FlaskForm):
    question = StringField("question", validators=[DataRequired("会话名称必传")])
    conversation_type = StringField("conversation_type", validators=[DataRequired("会话类型必传")])