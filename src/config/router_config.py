#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 15:45
@Author  : tianshiyang
@File    : router_config.py
"""
from flask import Flask

from router import account_blueprint, dataset_blueprint, ai_blueprint, \
    document_blueprint, sales_blueprint, customer_blueprint


# 注册路由
def init_flask_router(app: Flask):
    for blue_print in [
        account_blueprint, # 账号模块
        dataset_blueprint, # 知识库模块
        document_blueprint, # 知识库文档模块
        ai_blueprint, # AI相关模块
        sales_blueprint, # 后台服务，销售模块
        customer_blueprint, # 客户模块
    ]:
        app.register_blueprint(
            blue_print
        )