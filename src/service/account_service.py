#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 10:14
@Author  : tianshiyang
@File    : account_service.py
"""
from config.db_config import db
from pkg.exception import FailException
from pkg.security import check_password_hash, generate_password_hash
from schema.account_schema import AccountUserLoginReq, AccountUserRegistrationReq
from model.account import Account

def get_user_info(username: str, email: str) -> Account:
    """通过用户名或邮箱查询用户"""
    # 注意：使用 or_ 而不是 or，因为 SQLAlchemy 需要特殊处理
    from sqlalchemy import or_
    user = db.session.query(Account).filter(
        or_(Account.username == username, Account.email == email)
    ).first()
    return user

def account_user_registration_service(req: AccountUserRegistrationReq) -> Account:
    """用户注册"""
    if get_user_info(req.username.data, req.email.data) is not None:
        raise FailException("用户名或邮箱已存在")

    # 创建账户对象
    account = Account(
        username=req.username.data,
        email=req.email.data,
        password_hash=generate_password_hash(req.password.data),
        avatar_url=req.avatar_url.data if req.avatar_url.data else "",
    ).create()

    return account

# 用户登录
def account_user_login_service(req: AccountUserLoginReq) -> Account:
    """
    用户登录服务
    从 PostgreSQL 数据库查询用户并验证密码
    """
    username = req.username.data
    password = req.password.data
    
    # 从数据库查询用户
    user = db.session.query(Account).filter(Account.username == username).first()
    if not user:
        raise FailException("用户不存在")
    if not check_password_hash(user.password_hash, password):
        raise FailException("用户名或密码错误")
    
    # 登录成功，返回用户信息（不返回密码）
    return user