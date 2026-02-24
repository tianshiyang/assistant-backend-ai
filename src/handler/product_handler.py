#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/17 20:56
@Author  : tianshiyang
@File    : product_handler.py
"""
from flask import request

from pkg.response import validate_error_json, success_json
from schema.product_schema import GetProductCategoryListSchema, GetProductListSchema
from service.product_service import get_product_category_list_service, get_product_list_service
from utils import transform_pagination_data


def get_product_category_list_handler():
    """获取商品分类列表"""
    req = GetProductCategoryListSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    paginate = get_product_category_list_service(req)
    return success_json(transform_pagination_data(paginate))

def get_product_list_handler():
    """获取商品列表"""
    req = GetProductListSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    paginate = get_product_list_service(req)
    print(transform_pagination_data(paginate))
    return success_json(transform_pagination_data(paginate))
