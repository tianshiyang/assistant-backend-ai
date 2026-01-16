#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 00:06
@Author  : tianshiyang
@File    : account_handler.py
"""
from datetime import timedelta

from flask_jwt_extended import create_access_token

from pkg.response import validate_error_json, success_json, success_message
from schema.account_schema import AccountUserLoginReq, AccountUserRegistrationReq
from service.account_service import account_user_login_service, account_user_registration_service

def generated_token(user_id):
    """生成用户token"""
    token = create_access_token(
        identity={
            "user_id": user_id,
        },
        expires_delta=timedelta(days=30)
    )
    return token

def account_user_registration_handler() -> str:
    """用户注册"""
    req = AccountUserRegistrationReq()
    if not req.validate():
        return validate_error_json(req.errors)
    account = account_user_registration_service(req)
    token = generated_token(account.id)
    return success_json({
        "token": token,
    })

def account_user_login_handler() -> str:
    """用户登录"""
    req = AccountUserLoginReq()
    if not req.validate():
        return validate_error_json(req.errors)
    user = account_user_login_service(req)
    token = generated_token(user.id)
    return success_json({
        "token": token,
    })