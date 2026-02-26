#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/25 22:17
@Author  : tianshiyang
@File    : order_schema.py
"""
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired

from schema.base_schema import PaginationSchema


class GetOrderListSchema(PaginationSchema):
    """获取商品列表"""
    order_no = StringField(validators=[])