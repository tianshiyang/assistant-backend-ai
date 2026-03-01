#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13 15:44
@Author  : tianshiyang
@File    : __init__.py

router_config 延迟导入，避免 config 被 import 时拉入 router -> handler -> service -> model，
与 model.base_model -> config.db_config 形成循环。
"""
from .app_config import init_flask_app_config
from .exception_config import init_flask_error
from .db_config import init_db_config
from .jwt_config import init_flask_jwt_config
from .celery_config import init_celery_config
from .redis_config import init_redis_config
from .log_config import init_log_config


def init_flask_router(app):
    """延迟导入 router_config，仅在调用时加载路由，避免循环依赖。"""
    from .router_config import init_flask_router as _init
    return _init(app)


__all__ = [
    "init_flask_app_config",
    "init_flask_router",
    "init_flask_error",
    "init_db_config",
    "init_flask_jwt_config",
    "init_celery_config",
    "init_redis_config",
    "init_log_config",
]