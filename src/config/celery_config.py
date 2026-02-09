#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Celery 配置模块
- Redis 作为 broker / result_backend
- FlaskTask 保证每个任务都有 app context + 正确的 session 生命周期
"""
import os
import logging
from urllib.parse import quote_plus

from celery import Celery, Task
from celery.signals import setup_logging
from flask import Flask

from .log_config import init_log_config

logger = logging.getLogger(__name__)


# ─── Celery worker 日志 ──────────────────────────────────────────
@setup_logging.connect
def _config_celery_logging(**kwargs):
    """Worker 启动时复用 Flask 同一套日志配置。"""
    init_log_config(app=None, force=True)


# ─── 工具函数 ────────────────────────────────────────────────────
def _build_redis_url(db: int) -> str:
    """拼接 redis://:password@host:port/db。"""
    host = os.getenv("REDIS_HOST", "localhost")
    port = os.getenv("REDIS_PORT", "6379")
    password = os.getenv("REDIS_PASSWORD", "")
    return f"redis://:{quote_plus(password)}@{host}:{port}/{db}"


# ─── 初始化 ──────────────────────────────────────────────────────
def init_celery_config(app: Flask) -> Celery:
    """创建 Celery 实例并绑定到 Flask app。"""
    broker_url = _build_redis_url(int(os.getenv("CELERY_BROKER_DB", "0")))
    backend_url = _build_redis_url(int(os.getenv("CELERY_RESULT_BACKEND_DB", "1")))

    app.config.from_mapping(
        CELERY=dict(
            broker_url=broker_url,
            result_backend=backend_url,
            task_ignore_result=True,
            task_serializer="json",
            result_serializer="json",
            accept_content=["json"],
            timezone="UTC",
            enable_utc=True,
            beat_schedule={
                "cleanup-old-logs": {
                    "task": "src.task.cleanup_log_task.cleanup_old_logs_task",
                    "schedule": 86400.0,
                    "options": {"expires": 3600},
                },
            },
        ),
    )

    class FlaskTask(Task):
        """确保每个任务都有 Flask app context，并正确管理 DB session 生命周期。"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                from config.db_config import db

                # 任务开始前：移除可能过期的 session，获取新连接
                try:
                    db.session.remove()
                except Exception:
                    pass

                try:
                    return self.run(*args, **kwargs)
                finally:
                    # 任务结束后：归还连接到连接池
                    try:
                        db.session.remove()
                    except Exception:
                        pass

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    celery_app.autodiscover_tasks(["src.task"], force=True)
    app.extensions["celery"] = celery_app
    return celery_app
