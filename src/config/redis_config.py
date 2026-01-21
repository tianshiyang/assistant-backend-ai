#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/21 10:32
@Author  : tianshiyang
@File    : redis_config.py
"""
import os

from flask import Flask


def init_redis_config(app: Flask):
    # Redis配置
    app.config['REDIS_HOST'] = os.getenv("REDIS_HOST")
    app.config['REDIS_PORT'] = os.getenv("REDIS_PORT")
    app.config['REDIS_USERNAME'] = os.getenv("REDIS_USERNAME")
    app.config['REDIS_PASSWORD'] = os.getenv("REDIS_PASSWORD")
    app.config['REDIS_DB'] = os.getenv("REDIS_DB")
    app.config['REDIS_USE_SSL'] = bool(os.getenv("REDIS_USE_SSL"))