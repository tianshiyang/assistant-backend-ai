#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/16 15:54
@Author  : tianshiyang
@File    : jwt_config.py
"""
import os

from flask import Flask
from flask_jwt_extended import JWTManager

from pkg.response.response import unauthorized_json


def init_flask_jwt_config(app: Flask):
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def custom_unauthorized(err):
        return unauthorized_json()
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Token 过期回调"""
        return unauthorized_json()
    
    @jwt.invalid_token_loader
    def invalid_token_callback(err):
        """无效 Token 回调"""
        return unauthorized_json()

