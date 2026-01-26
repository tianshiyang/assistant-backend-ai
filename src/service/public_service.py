#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 21:07
@Author  : tianshiyang
@File    : public_router.py
"""
from entities.ai import Skills


def get_skills_dict_service():
    result = [
        {
            "label": skill.label,
            "value": skill.value
        } for skill in Skills]
    return result