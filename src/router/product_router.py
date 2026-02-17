#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/17 20:55
@Author  : tianshiyang
@File    : product_router.py
"""
from flask import Blueprint

from handler.product_handler import get_product_category_list_handler

product_blueprint = Blueprint("product_blueprint", __name__, url_prefix="")

# 获取商品分类列表
product_blueprint.add_url_rule("/api/manage/product/category/list", view_func=get_product_category_list_handler)