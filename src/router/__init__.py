#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/12 22:48
@Author  : tianshiyang
@File    : __init__.py.py
"""
from .account_routes import account_blueprint
from .dataset_routes import dataset_blueprint
from .document_router import document_blueprint
from .ai_router import ai_blueprint
from .public_router import public_blueprint

__all__ = [
    "account_blueprint",
    "dataset_blueprint",
    "document_blueprint",
    "ai_blueprint",
    "public_blueprint"
]