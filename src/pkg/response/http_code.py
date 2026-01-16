#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 11:21
@Author  : tianshiyang
@File    : http_code.py
"""
from enum import Enum


class HttpCode(str, Enum):
    """HTTP基础业务状态码"""
    SUCCESS = "success"
    ERROR = "error"
    LOGIN_EXPIRED = "login_expired" # 登录过期
    UNAUTHORIZED = "unauthorized"  # 未授权
    FORBIDDEN = "forbidden"  # 无权限
    VALIDATE_ERROR = "validate_error"  # 数据验证错误