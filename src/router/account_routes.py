#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/12 23:11
@Author  : tianshiyang
@File    : account_routes.py
"""
from flask import Blueprint

from handler.account_handler import account_user_login_handler, account_user_registration_handler

"""账号相关接口"""
account_blueprint = Blueprint("api", __name__, url_prefix="")

account_blueprint.add_url_rule("/api/account/login", methods=["POST"], view_func=account_user_login_handler)
account_blueprint.add_url_rule("/api/account/registration", methods=["POST"], view_func=account_user_registration_handler)

