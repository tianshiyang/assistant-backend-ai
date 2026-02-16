#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/16
@Author  : tianshiyang
@File    : customer_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Optional

from schema.base_schema import PaginationSchema


class CreateCustomerSchema(FlaskForm):
    """新增客户"""
    name = StringField("name", validators=[DataRequired(message="客户姓名不能为空")])
    email = StringField("email", validators=[Optional()])
    phone = StringField("phone", validators=[Optional()])
    status = IntegerField("status", validators=[Optional()], default=1)


class UpdateCustomerSchema(FlaskForm):
    """编辑客户"""
    customer_id = IntegerField("customer_id", validators=[DataRequired(message="客户ID不能为空")])
    name = StringField("name", validators=[Optional()])
    email = StringField("email", validators=[Optional()])
    phone = StringField("phone", validators=[Optional()])
    status = IntegerField("status", validators=[Optional()])


class GetCustomerDetailSchema(FlaskForm):
    """根据id查询客户详情"""
    customer_id = IntegerField("customer_id", validators=[DataRequired(message="客户ID不能为空")])


class GetCustomerListSchema(PaginationSchema):
    """客户列表查询"""
    customer_no = StringField("customer_no", validators=[Optional()])
    name = StringField("name", validators=[Optional()])
    phone = StringField("phone", validators=[Optional()])
    status = IntegerField("status", validators=[Optional()])
