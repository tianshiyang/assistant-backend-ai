#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 21:04
@Author  : tianshiyang
@File    : public_handler.py
"""
from flask import Blueprint

from handler.public_handler import get_skills_dict_handler

public_blueprint = Blueprint("public", __name__, url_prefix="/")

public_blueprint.add_url_rule("/api/public/get_skills_dict", view_func=get_skills_dict_handler)