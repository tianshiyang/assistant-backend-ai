#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/20 16:02
@Author  : tianshiyang
@File    : document_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, URL

from schema.base_schema import PaginationSchema


class DocumentUploadToMilvusSchema(FlaskForm):
    dataset_id = StringField("dataset_id", validators=[
        DataRequired("知识库ID必传")
    ])

    oss_url = StringField("oss_url", validators=[
        URL(message="格式必须是url格式"),
        DataRequired("oss链接必传")
    ])


class DocumentGetAllListSchema(PaginationSchema):
    dataset_id = StringField("dataset_id", validators=[
        DataRequired("知识库id必传"),
    ])
    name = StringField("name", validators=[
    ])

class DocumentDeleteSchema(FlaskForm):
    document_id = StringField("document_id", validators=[
        DataRequired("文档id必传")
    ])