#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 10:14
@Author  : tianshiyang
@File    : account_service.py
"""
from pkg.exception import UnauthorizedException
from pkg.security import check_password_hash, generate_password_hash
from schema.account_schema import AccountUserLoginReq

USER_DATABASE = {
    "tianshiyang": {
        "username": "tianshiyang",
        # 密码 'tianshiyang' 的哈希值（使用 pbkdf2:sha256 方法）
        "password_hash": "pbkdf2:sha256:1000000$WAlLEA2aQgzqD65l$2dda0068a30132fa59cdf08c6ac33325ef5e6808f6f42409277d1d30cc2be4f8"
    }
}


# 用户登录
def account_user_login_service(req: AccountUserLoginReq):
    username = req.username.data
    password = req.password.data
    
    # 查询用户
    user = USER_DATABASE.get(username)
    if not user:
        raise UnauthorizedException("用户名或密码错误")
    
    # 验证密码
    if not check_password_hash(user["password_hash"], password):
        raise UnauthorizedException("用户名或密码错误")

    print(generate_password_hash(password))
    
    # 登录成功，返回用户信息（不返回密码）
    return {
        "username": user["username"],
        "message": "登录成功"
    }