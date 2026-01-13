#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 15:44
@Author  : tianshiyang
@File    : __init__.py.py
"""
from .app_config import init_flask_app_config
from .router_config import init_flask_router
from .exception_config import init_flask_error

__all__ = [
    "init_flask_app_config",
    "init_flask_router",
    "init_flask_error",
]