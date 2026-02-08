#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 18:26
@Author  : tianshiyang
@File    : ai_entity.py
"""
from enum import Enum




class Skills(str, Enum):
    """AI技能"""
    DATASET_RETRIEVER = ("dataset_retriever", "知识库检索")
    WEB_SEARCH = ("web_search", "联网搜索")
    # TEXT_TO_SQL = ("text_to_sql", "文本转SQL")

    def __new__(cls, value: str, label: str):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj