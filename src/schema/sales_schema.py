#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/15 18:25
@Author  : tianshiyang
@File    : sales_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


class GetSalesByIdSchema(FlaskForm):
    sales_id = IntegerField('sales_id', validators=[DataRequired()])