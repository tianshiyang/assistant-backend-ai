#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 10:14
@Author  : tianshiyang
@File    : account_service.py
"""
from pkg.exception import UnauthorizedException
from schema.account_schema import AccountUserLoginReq


# 用户登录
def account_user_login_service(req: AccountUserLoginReq):
    if req.username.data != "tianshiyang" or req.password.data != "tianshiyang":
        raise UnauthorizedException()
    return {
        "username": req.username.data,
        "password": req.password.data
    }