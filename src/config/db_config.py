#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13
@Author  : tianshiyang
@File    : db_config.py

数据库配置 —— 连接池 + Session 生命周期管理

关键设计：
1. 连接池（SQLAlchemy QueuePool）
   - pool_size      常驻连接数（默认 10）
   - max_overflow   高峰额外连接（默认 20）
   - pool_timeout   等待可用连接的超时（默认 30s）
   - pool_recycle   连接回收周期（默认 1800s），防止数据库端主动断开
   - pool_pre_ping  使用前自动检测连接有效性（Celery 长驻进程必需）

2. Session 生命周期（Flask-SQLAlchemy 默认行为，无需手动管理）
   - 每个请求结束时 Flask-SQLAlchemy 自动调用 db.session.remove()
     归还连接到连接池（不是关闭物理连接）。
   - Celery 任务中通过 FlaskTask.__call__ 在任务前后做 session.remove()，
     与 HTTP 请求保持一致。
   - 业务代码**不需要**手动 close/remove session。
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db_config(app: Flask) -> None:
    """初始化数据库配置与连接池。"""
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    # ── 连接池参数 ──
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_size": int(os.getenv("DB_POOL_SIZE", "10")),
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "20")),
        "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "300")),
        "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "1800")),
        "pool_pre_ping": True,
    }

    db.init_app(app)


def get_db() -> SQLAlchemy:
    """获取 SQLAlchemy 实例。"""
    return db
