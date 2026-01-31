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
from schema.schema import ListField


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

class ConversationDeleteSchema(FlaskForm):
    """删除会话"""
    conversation_id = StringField("conversation_id", validators=[
        DataRequired("会话id必传")
    ])