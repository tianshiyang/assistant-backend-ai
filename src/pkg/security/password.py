#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13
@Author  : tianshiyang
@File    : password.py
密码哈希和验证工具
使用 Werkzeug 的 security 模块（Flask 内置，无需额外依赖）
"""
from werkzeug.security import generate_password_hash as werkzeug_generate_password_hash
from werkzeug.security import check_password_hash as werkzeug_check_password_hash


def generate_password_hash(password: str, method: str = 'pbkdf2:sha256') -> str:
    """生成hash密码"""
    return werkzeug_generate_password_hash(password, method=method)


def check_password_hash(pwhash: str, password: str) -> bool:
    """检验密码是否正确"""
    return werkzeug_check_password_hash(pwhash, password)
