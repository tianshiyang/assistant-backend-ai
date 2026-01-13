#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 00:06
@Author  : tianshiyang
@File    : account_handler.py
"""
from schema.account_schema import AccountUserLoginReq
from service.account_service import account_user_login_service


# 用户登录
def account_user_login_handler() -> str:
    req = AccountUserLoginReq()
    if not req.validate():
        return '222'
    resp = account_user_login_service(req)
    return resp