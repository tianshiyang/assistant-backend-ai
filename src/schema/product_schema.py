#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/17 20:57
@Author  : tianshiyang
@File    : product_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired

from schema.base_schema import PaginationSchema


class GetProductCategoryListSchema(PaginationSchema):
    category_name = StringField(default="", validators=[])

class GetProductListAllSchema(FlaskForm):
    name = StringField(default="", validators=[])

class GetProductListSchema(PaginationSchema):
    name = StringField(default="", validators=[])
    category_id = StringField(default="", validators=[])
    product_no = StringField(default="", validators=[])

class GetProductDetailSchema(FlaskForm):
    id = StringField(default="", validators=[
        DataRequired("商品id必传")
    ])

class ProductUpdateSchema(FlaskForm):
    id = StringField(default="", validators=[
        DataRequired("商品id必传")
    ])
    name = StringField(default="", validators=[])
    category_id = StringField(default="", validators=[])
    standard_price = StringField(default="", validators=[])
    cost_price = StringField(default="", validators=[])