#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/20 16:36
@Author  : tianshiyang
@File    : document_entities.py
"""
from enum import Enum


class DocumentStatus(str, Enum):
    PARSING = "parsing" # 解析中
    COMPLETED = "completed" # 完成
    ERROR = "error" # 解析失败