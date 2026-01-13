#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 11:45
@Author  : tianshiyang
@File    : exception.py
"""
from dataclasses import field
from typing import Any

from pkg.response.http_code import HttpCode


class CustomException(Exception):
    """基础自定义异常信息"""
    code: HttpCode = HttpCode.ERROR
    message: str = ""
    data: Any = field(default_factory=dict)

    def __init__(self, message: str = None, data: Any = None):
        super().__init__()
        self.message = message
        self.data = data

class FailException(CustomException):
    """通用失败异常"""
    pass

class UnauthorizedException(CustomException):
    """未授权异常"""
    code = HttpCode.UNAUTHORIZED


class ForbiddenException(CustomException):
    """无权限异常"""
    code = HttpCode.FORBIDDEN


class ValidateErrorException(CustomException):
    """数据验证异常"""
    code = HttpCode.VALIDATE_ERROR
