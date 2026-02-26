#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/25 22:16
@Author  : tianshiyang
@File    : order_handler.py
"""
from flask import request

from pkg.response import validate_error_json, success_json, success_message
from schema.order_schema import GetOrderListSchema, CreateOrderSchema, PayOrderSchema, GetOrderDetailSchema, \
    CancelPayOrderSchema
from service.order_service import get_order_list_service, create_order_service, pay_order_service, \
    get_order_detail_service, cancel_pay_order_service
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

def get_order_detail_handler():
    """获取订单详情"""
    req = GetOrderDetailSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    order = get_order_detail_service(req.order_id.data)
    return success_json(order.to_dict())

def pay_order_handler():
    """支付订单"""
    req = PayOrderSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    pay_order_service(req)
    return success_json("支付成功")

def cancel_pay_order_handler():
    """取消支付"""
    req = CancelPayOrderSchema()

    print(req.order_id.data, '-a-a-aa-a--a')
    if not req.validate():
        return validate_error_json(req.errors)
    cancel_pay_order_service(req)
    return success_message("取消订单成功")
