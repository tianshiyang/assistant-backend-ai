#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/16 15:54
@Author  : tianshiyang
@File    : jwt_config.py
"""
import os

from flask import Flask
from flask_jwt_extended import JWTManager


def init_flask_jwt_config(app: Flask):
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    JWTManager(app)