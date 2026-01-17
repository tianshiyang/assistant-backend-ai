#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/18 00:41
@Author  : tianshiyang
@File    : base_entity.py
"""
from typing import TypeVar, Generic

T = TypeVar("T")
class Pagination(Generic[T]):
    total: int
    pages: int
    items: list[T]