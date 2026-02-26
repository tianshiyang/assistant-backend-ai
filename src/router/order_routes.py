#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/25 22:13
@Author  : tianshiyang
@File    : order_routes.py
"""
from flask import Blueprint

from handler.order_handler import get_order_list_handler, create_order_handler, pay_order_handler, get_order_detail_handler, cancel_pay_order_handler

order_blueprint = Blueprint("order", __name__)

# 获取商品订单列表
order_blueprint.add_url_rule("/api/manage/order/list", view_func=get_order_list_handler)

# 新增订单
order_blueprint.add_url_rule("/api/manage/order/create", methods=["POST"], view_func=create_order_handler)

# 获取订单详情
order_blueprint.add_url_rule("/api/manage/order/detail", view_func=get_order_detail_handler)

# 支付
order_blueprint.add_url_rule("/api/manage/order/pay", methods=["POST"], view_func=pay_order_handler)

# 取消支付
order_blueprint.add_url_rule("/api/manage/order/cancel_pay", methods=["POST"], view_func=cancel_pay_order_handler)