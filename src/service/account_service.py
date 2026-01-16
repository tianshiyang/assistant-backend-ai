#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 10:14
@Author  : tianshiyang
@File    : account_service.py
"""
from config.db_config import db
from pkg.exception import UnauthorizedException
from pkg.security import check_password_hash
from schema.account_schema import AccountUserLoginReq
from model.account import Account


# 用户登录
def account_user_login_service(req: AccountUserLoginReq):
    """
    用户登录服务
    从 PostgreSQL 数据库查询用户并验证密码
    """
    username = req.username.data
    password = req.password.data
    
    # 从数据库查询用户
    user = db.session.query(Account).filter(Account.username == username).first()
    print(user)
    if not user:
        raise UnauthorizedException("用户不存在")
    if not check_password_hash(user.password_hash, password):
        raise UnauthorizedException("用户名或密码错误")
    
    # 登录成功，返回用户信息（不返回密码）
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "message": "登录成功"
    }