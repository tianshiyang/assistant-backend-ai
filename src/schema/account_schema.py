#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 00:13
@Author  : tianshiyang
@File    : account_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField, URLField, EmailField
from wtforms.validators import DataRequired, Length

class AccountUserRegistrationReq(FlaskForm):
    username = StringField("username", validators=[
        DataRequired("用户名不能为空"),
        Length(min=4, max=32, message="用户名4-32位")
    ])
    password = StringField("password", validators=[
        DataRequired("密码必填"),
        Length(min=8, max=32, message="密码8-32位")
    ])
    avatar_url = URLField("avatar_url", validators=[
        DataRequired("头像必传"),
    ])
    email = EmailField("email", validators=[
        DataRequired("email必传"),
    ])

class AccountUserLoginReq(FlaskForm):
    """用户登录schema"""
    username = StringField("username", validators=[
        DataRequired("用户名必填"),
        Length(min=4, max=32, message="用户名4-32位")
    ])
    password = StringField("password", validators=[
        DataRequired("密码必填"),
        Length(min=8, max=32, message="密码8-32位")
    ])