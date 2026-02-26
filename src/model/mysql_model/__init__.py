#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/15 18:12
@Author  : tianshiyang
@File    : __init__.py.py
"""
from .customer import Customer
from .product import Product, ProductCategory
from .sales_person import SalesPerson
from .orders import Orders, OrderItem

__all__ = [
    'Customer',
    'Product',
    'ProductCategory',
    'SalesPerson',
    "Orders",
    "OrderItem",
]