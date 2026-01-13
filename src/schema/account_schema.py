#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 00:13
@Author  : tianshiyang
@File    : account_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class AccountUserLoginReq(FlaskForm):
    username = StringField("username", validators=[
        DataRequired("用户名必填"),
        Length(min=8, max=32, message="用户名8-32位")
    ])
    password = StringField("password", validators=[
        DataRequired("密码必填"),
        Length(min=8, max=32, message="密码8-32位")
    ])