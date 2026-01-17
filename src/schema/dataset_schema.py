#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/17 22:51
@Author  : tianshiyang
@File    : dataset_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CreateDatasetSchema(FlaskForm):
    name = StringField("name", validators=[
        DataRequired("知识库名称必填"),
        Length(max=100),
    ])
    icon = StringField("icon", validators=[
        DataRequired("知识库icon必填")
    ])
    description = StringField("description", validators=[
        DataRequired("知识库名称必填")
    ])