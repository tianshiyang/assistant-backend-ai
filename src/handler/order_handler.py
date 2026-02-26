#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/25 22:16
@Author  : tianshiyang
@File    : order_handler.py
"""
from flask import request

from pkg.response import validate_error_json, success_json, success_message
from schema.order_schema import GetOrderListSchema, CreateOrderSchema
from service.order_service import get_order_list_service, create_order_service
from utils import transform_pagination_data


def get_order_list_handler():
    """获取商品列表"""
    req = GetOrderListSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    pagination = get_order_list_service(req)
    return success_json(transform_pagination_data(pagination))

def create_order_handler():
    """新增订单"""
    req = CreateOrderSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    create_order_service(req)
    return success_message("创建成功")
