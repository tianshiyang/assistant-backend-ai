#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 18:23
@Author  : tianshiyang
@File    : ai_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, AnyOf

from entities.ai import Skills


class AIChatSchema(FlaskForm):
    """聊天"""
    dataset_ids = StringField("dataset_ids", validators=[])
    skills = StringField("skills", validators=[
        AnyOf(
            values=[item.value for item in Skills],
            message="技能类型错误"
        )
    ])