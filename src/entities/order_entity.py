#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/26 15:27
@Author  : tianshiyang
@File    : order_entity.py
"""
from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "created"
    FAILED = "failed"
    COMPLETED = "completed"
    PAID = "paid"
    CANCELED = "canceled"