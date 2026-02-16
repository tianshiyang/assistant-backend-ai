#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/16
@Author  : tianshiyang
@File    : customer_router.py
客户模块路由
"""
from flask import Blueprint

from handler.customer_handler import (
    create_customer_handler,
    update_customer_handler,
    get_customer_list_handler,
    get_customer_detail_handler,
)

customer_blueprint = Blueprint("customer", __name__, url_prefix="")

# 新增客户
customer_blueprint.add_url_rule(
    "/api/manage/customer/create",
    methods=["POST"],
    view_func=create_customer_handler,
)

# 编辑客户
customer_blueprint.add_url_rule(
    "/api/manage/customer/update",
    methods=["POST"],
    view_func=update_customer_handler,
)

# 查询客户列表
customer_blueprint.add_url_rule(
    "/api/manage/customer/list",
    methods=["GET"],
    view_func=get_customer_list_handler,
)

# 根据id查询客户详情
customer_blueprint.add_url_rule(
    "/api/manage/customer/detail",
    methods=["GET"],
    view_func=get_customer_detail_handler,
)
