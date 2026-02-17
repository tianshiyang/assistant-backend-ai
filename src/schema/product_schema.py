#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/17 20:57
@Author  : tianshiyang
@File    : product_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField

from schema.base_schema import PaginationSchema


class GetProductCategoryListSchema(PaginationSchema):
    category_name = StringField(default="", validators=[])