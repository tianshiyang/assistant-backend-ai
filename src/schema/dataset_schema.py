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
    """创建知识库"""
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

class GetDataSetDetailSchema(FlaskForm):
    """获取知识库详情"""
    dataset_id = StringField("dataset_id", validators=[
        DataRequired("知识库id必传")
    ])

class UpdateDatasetSchema(FlaskForm):
    """更新知识库"""
    dataset_id = StringField("dataset_id", validators=[
        DataRequired("知识库id必传")
    ])
    name = StringField("name", validators=[
        Length(max=100),
    ])
    icon = StringField("icon", validators=[])
    description = StringField("description", validators=[])