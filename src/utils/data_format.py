#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/18 00:59
@Author  : tianshiyang
@File    : data_format.py
"""
from typing import Any

from entities.base_entity import Pagination


def transform_pagination_data(result: Pagination) -> dict[str, Any]:
    """格式化列表类型数据"""
    response = {
        "total": result.total,
        "list": [item.to_dict() for item in result.items],
        "pages": result.pages,
    }
    return response