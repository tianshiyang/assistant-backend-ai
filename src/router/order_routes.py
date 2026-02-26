#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/25 22:13
@Author  : tianshiyang
@File    : order_routes.py
"""
from flask import Blueprint

from handler.order_handler import get_order_list_handler

order_blueprint = Blueprint("order", __name__)

order_blueprint.add_url_rule("/api/manage/order/list", view_func=get_order_list_handler)