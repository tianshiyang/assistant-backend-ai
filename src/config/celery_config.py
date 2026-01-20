#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/20 18:07
@Author  : tianshiyang
@File    : celery_config.py
"""
import os

from celery import Celery, Task
from flask import Flask


def _build_redis_url(host: str, port: str, password: str = None, db: int = 0) -> str:
    """
    构建 Redis 连接 URL
    
    Args:
        host: Redis 主机地址
        port: Redis 端口
        password: Redis 密码（可选）
        db: Redis 数据库编号
    
    Returns:
        str: Redis 连接 URL
    """
    if password:
        return f"redis://:{password}@{host}:{port}/{db}"
    else:
        return f"redis://{host}:{port}/{db}"


def celery_config(app: Flask):
    """
    配置 Celery
    
    环境变量说明:
    - REDIS_HOST: Redis 主机地址（默认: localhost）
    - REDIS_PORT: Redis 端口（默认: 6379）
    - REDIS_PASSWORD: Redis 密码（可选）
    - CELERY_BROKER_DB: Celery broker 使用的 Redis 数据库编号（默认: 0）
    - CELERY_RESULT_BACKEND_DB: Celery result backend 使用的 Redis 数据库编号（默认: 1）
    - CELERY_TASK_IGNORE_RESULT: 是否忽略任务结果（默认: False）
    - CELERY_RESULT_EXPIRES: 结果过期时间，秒（默认: 3600）
    - CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP: 启动时重试连接（默认: True）
    """
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = os.getenv('REDIS_PORT', '6379')
    redis_password = os.getenv('REDIS_PASSWORD', '')
    broker_db = int(os.getenv('CELERY_BROKER_DB', '0'))
    result_db = int(os.getenv('CELERY_RESULT_BACKEND_DB', '1'))
    
    # 构建 Redis URL
    broker_url = _build_redis_url(redis_host, redis_port, redis_password, broker_db)
    result_backend_url = _build_redis_url(redis_host, redis_port, redis_password, result_db)
    
    app.config.from_mapping(
        CELERY={
            "broker_url": broker_url,
            "result_backend": result_backend_url,
            "task_ignore_result": os.getenv("CELERY_TASK_IGNORE_RESULT", "False").lower() == "true",
            "result_expires": int(os.getenv("CELERY_RESULT_EXPIRES", "3600")),  # 结果过期时间（秒）
            "broker_connection_retry_on_startup": os.getenv("CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP", "True").lower() == "true",
            "broker_connection_retry": True,  # 启用连接重试
            "broker_connection_max_retries": 10,  # 最大重试次数
            "task_serializer": "json",  # 任务序列化格式
            "result_serializer": "json",  # 结果序列化格式
            "accept_content": ["json"],  # 接受的内容类型
            "timezone": "UTC",  # 时区
            "enable_utc": True,  # 启用 UTC
        }
    )
    
    class FlaskTask(Task):
        """Flask 应用上下文的 Celery 任务"""
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app