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
    # 配置 SECRET_KEY（Flask-WTF 需要）
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # 禁用 CSRF（API 项目通常不需要 CSRF 保护，使用 token 认证）
    app.config['WTF_CSRF_ENABLED'] = False

    # 跨域配置
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "supports_credentials": True,
            # "methods": ["GET", "POST"],
            # "allow_headers": ["Content-Type"],
        }
    })
