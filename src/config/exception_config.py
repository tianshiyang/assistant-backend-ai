#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 15:46
@Author  : tianshiyang
@File    : exception_config.py
"""
from flask import Flask

from pkg.exception.exception import CustomException
from pkg.response import json, Response, HttpCode

def _register_error_handler(error: Exception):
    if isinstance(error, CustomException):
        return json(Response(
            code=error.code,
            message=error.message,
            data=error.data,
        ))
    return json(Response(
        code=HttpCode.ERROR,
        message=str(error),
        data={},
    ))

# 自定义异常
def init_flask_error(app: Flask):
    app.register_error_handler(Exception, _register_error_handler)