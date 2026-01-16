#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 00:06
@Author  : tianshiyang
@File    : account_handler.py
"""
from pkg.response import validate_error_json, success_json, success_message
from schema.account_schema import AccountUserLoginReq, AccountUserRegistrationReq
from service.account_service import account_user_login_service, account_user_registration_service


def account_user_registration_handler() -> str:
    """用户注册"""
    req = AccountUserRegistrationReq()
    if not req.validate():
        return validate_error_json(req.errors)
    account_user_registration_service(req)
    return success_message("注册成功！")

def account_user_login_handler() -> str:
    """用户登录"""
    req = AccountUserLoginReq()
    if not req.validate():
        return validate_error_json(req.errors)
    resp = account_user_login_service(req)
    return success_json(resp)