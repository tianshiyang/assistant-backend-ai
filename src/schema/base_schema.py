#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/18 00:16
@Author  : tianshiyang
@File    : base_schema.py
"""
from flask_wtf import FlaskForm
from wtforms.fields import IntegerField


class PaginationSchema(FlaskForm):
    page_size = IntegerField(
        "page_size",
        default=10,
        validators=[]
    )
    page_no = IntegerField(
        "page_no",
        default=1,
        validators=[]
    )
