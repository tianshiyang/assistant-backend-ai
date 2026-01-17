#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/17 23:45
@Author  : tianshiyang
@File    : dataset_entities.py
"""
from enum import Enum

class DatasetStatus(str, Enum):
    # 知识库状态: parsing文件解析中 -> 不可选择此数据库，using -> 使用中
    USING = "using" # 使用中
    PARING = "paring" # 解析中