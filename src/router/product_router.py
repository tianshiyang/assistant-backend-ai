#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/17 20:55
@Author  : tianshiyang
@File    : product_router.py
"""
from flask import Blueprint

from handler.product_handler import get_product_category_list_handler, get_product_list_handler, \
    get_product_list_all_handler, get_product_detail_handler, update_product_handler, create_product_handler, \
    delete_product_handler, get_product_category_list_all_handler

product_blueprint = Blueprint("product_blueprint", __name__, url_prefix="")

# 获取商品分类列表
product_blueprint.add_url_rule("/api/manage/product/category/list", view_func=get_product_category_list_handler)

# 获取所有商品分类（不分页）
product_blueprint.add_url_rule("/api/manage/product/category/list/all", view_func=get_product_category_list_all_handler)

# 获取商品列表
product_blueprint.add_url_rule("/api/manage/product/list", view_func=get_product_list_handler)

# 获取所有商品不分页
product_blueprint.add_url_rule("/api/manage/product/list_all", view_func=get_product_list_all_handler)

# 获取商品详情
product_blueprint.add_url_rule("/api/manage/product/detail", view_func=get_product_detail_handler)

# 编辑商品信息
product_blueprint.add_url_rule("/api/manage/product/update", methods=["POST"], view_func=update_product_handler)

# 创建商品
product_blueprint.add_url_rule("/api/manage/product/create", methods=["POST"], view_func=create_product_handler)

# 删除商品
product_blueprint.add_url_rule("/api/manage/product/delete", methods=["POST"], view_func=delete_product_handler)
