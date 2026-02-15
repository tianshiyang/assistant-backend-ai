#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/15 18:25
@Author  : tianshiyang
@File    : sales_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired

from schema.base_schema import PaginationSchema


class GetSalesByIdSchema(FlaskForm):
    sales_id = IntegerField('sales_id', validators=[DataRequired()])

class GetAllSalesSchema(PaginationSchema):
    sales_name = StringField('sales_name', validators=[])
