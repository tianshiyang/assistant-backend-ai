#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 15:44
@Author  : tianshiyang
@File    : app_config.py
"""
from flask import Flask
import os
from flask_cors import CORS


def init_flask_app_config(app: Flask):
    # 配置 JSON 响应不转义中文字符
    app.config['JSON_AS_ASCII'] = False

    # 配置 SECRET_KEY（Flask-WTF 需要）
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # 禁用 CSRF（API 项目通常不需要 CSRF 保护，使用 token 认证）
    app.config['WTF_CSRF_ENABLED'] = False

    # Redis配置
    app.config['REDIS_HOST'] = os.getenv("REDIS_HOST")
    app.config['REDIS_PORT'] = os.getenv("REDIS_PORT")
    app.config['REDIS_USERNAME'] = os.getenv("REDIS_USERNAME")
    app.config['REDIS_PASSWORD'] = os.getenv("REDIS_PASSWORD")
    app.config['REDIS_DB'] = os.getenv("REDIS_DB")
    app.config['REDIS_USE_SSL'] = bool(os.getenv("REDIS_USE_SSL"))

    # 跨域配置
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "supports_credentials": True,
            # "methods": ["GET", "POST"],
            # "allow_headers": ["Content-Type"],
        }
    })
