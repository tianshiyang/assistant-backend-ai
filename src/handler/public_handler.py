#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 21:06
@Author  : tianshiyang
@File    : public_handler.py
"""
from pkg.response import success_json
from service.public_service import get_skills_dict_service


def get_skills_dict_handler():
    res = get_skills_dict_service()
    return success_json(res)