#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/25 22:16
@Author  : tianshiyang
@File    : order_handler.py
"""
from flask import request
from flask_jwt_extended import jwt_required

from pkg.response import validate_error_json, success_json, success_message
from schema.order_schema import GetOrderListSchema, CreateOrderSchema, PayOrderSchema, GetOrderDetailSchema, \
    CancelPayOrderSchema, DeleteOrderSchema
from service.order_service import get_order_list_service, create_order_service, pay_order_service, \
    get_order_detail_service, cancel_pay_order_service, delete_order_service
from utils import transform_pagination_data

@jwt_required()
def get_order_list_handler():
    """获取商品列表"""
    req = GetOrderListSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    pagination = get_order_list_service(req)
    return success_json(transform_pagination_data(pagination))

@jwt_required()
def create_order_handler():
    """新增订单"""
    req = CreateOrderSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    create_order_service(req)
    return success_message("创建成功")

@jwt_required()
def get_order_detail_handler():
    """获取订单详情"""
    req = GetOrderDetailSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    order = get_order_detail_service(req.order_id.data)
    return success_json(order.to_dict())

@jwt_required()
def pay_order_handler():
    """支付订单"""
    req = PayOrderSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    pay_order_service(req)
    return success_json("支付成功")

@jwt_required()
def cancel_pay_order_handler():
    """取消支付"""
    req = CancelPayOrderSchema()

    if not req.validate():
        return validate_error_json(req.errors)
    cancel_pay_order_service(req)
    return success_message("取消订单成功")

@jwt_required()
def delete_order_handler():
    req = DeleteOrderSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    delete_order_service(req)
    return success_message("删除订单成功")
