#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/15 18:19
@Author  : tianshiyang
@File    : sales_routes.py
"""
from flask import Blueprint

from handler.sales_handler import get_sales_by_id_handler

sales_blueprint = Blueprint("sales_router", __name__, url_prefix="")

# 获取销售详情信息
sales_blueprint.add_url_rule("/api/manage/sales/detail_by_id", view_func=get_sales_by_id_handler)
