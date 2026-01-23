#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 11:23
@Author  : tianshiyang
@File    : response.py
"""
import json as json_module
from dataclasses import dataclass, field, asdict
from typing import Any
from enum import Enum
import uuid

from flask import Response as FlaskResponse

from pkg.response.http_code import HttpCode


@dataclass
class Response:
    code: HttpCode = HttpCode.SUCCESS
    message: str = ""
    data: Any = field(default_factory=dict)


class JSONEncoder(json_module.JSONEncoder):
    """自定义 JSON 编码器，处理枚举、UUID 和其他特殊类型"""
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)


def json(data: Any = None) -> Any:
    """基础接口响应"""
    # 如果是 Response 对象，转换为字典
    if isinstance(data, Response):
        data_dict = asdict(data)
    else:
        data_dict = data
    
    # 使用 json.dumps 并设置 ensure_ascii=False 确保中文字符不被转义
    json_str = json_module.dumps(
        data_dict,
        ensure_ascii=False,
        cls=JSONEncoder
    )
    
    return FlaskResponse(
        json_str,
        status=200,
        mimetype='application/json; charset=utf-8'
    )

def success_json(data: Any = None) -> Any:
    """成功的数据响应"""
    return json(Response(data=data, message="", code=HttpCode.SUCCESS))

def error_json(data: Any = None) -> Any:
    """失败的数据响应"""
    return json(Response(data=data, message="", code=HttpCode.ERROR))

def unauthorized_json(data: Any = None) -> Any:
    """认证失败的数据相应"""
    return json(Response(data=data, message="认证失败", code=HttpCode.UNAUTHORIZED))

def validate_error_json(errors: dict = None) -> Any:
    """数据验证错误"""
    first_key = next(iter(errors))
    if first_key is not None:
        msg = errors.get(first_key)[0]
    else:
        msg = ""
    return json(Response(data=errors, message=msg, code=HttpCode.VALIDATE_ERROR))

def message(code: HttpCode = None, msg: str = ""):
    """基础的消息响应，固定返回消息提示，数据固定为空字典"""
    return json(Response(code=code, message=msg, data={}))

def success_message(msg: str = ""):
    """成功的消息响应"""
    return message(code=HttpCode.SUCCESS, msg=msg)


def error_message(msg: str = ""):
    """失败的消息响应"""
    return message(code=HttpCode.ERROR, msg=msg)