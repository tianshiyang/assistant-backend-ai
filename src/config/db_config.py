#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13
@Author  : tianshiyang
@File    : db_config.py

数据库配置 —— 连接池 + Session 生命周期管理

支持数据库：
  - PostgreSQL（默认，SQLALCHEMY_DATABASE_URI）
  - MySQL（通过 SQLALCHEMY_BINDS['mysql']，模型中声明 __bind_key__ = 'mysql' 即可使用）

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

# ── 通用连接池参数（PostgreSQL / MySQL 共用） ──
def _pool_options() -> dict:
    return {
        "pool_size": int(os.getenv("DB_POOL_SIZE", "10")),
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "20")),
        "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "300")),
        "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "1800")),
        "pool_pre_ping": True,
    }


def _build_mysql_uri() -> str:
    """从环境变量拼装 MySQL URI。"""
    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = os.getenv("MYSQL_PORT", "3306")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "")
    charset = os.getenv("MYSQL_CHARSET", "utf8mb4")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}"


def init_db_config(app: Flask) -> None:
    """初始化数据库配置与连接池。"""
    # ── PostgreSQL（默认库） ──
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    # 默认库连接池参数
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = _pool_options()

    # ── MySQL（绑定库，bind_key='mysql'） ──
    mysql_database = os.getenv("MYSQL_DATABASE", "")
    if mysql_database:
        app.config["SQLALCHEMY_BINDS"] = {
            "mysql": {
                "url": _build_mysql_uri(),
                "pool_size": int(os.getenv("MYSQL_POOL_SIZE", "10")),
                "max_overflow": int(os.getenv("MYSQL_MAX_OVERFLOW", "20")),
                "pool_timeout": int(os.getenv("MYSQL_POOL_TIMEOUT", "300")),
                "pool_recycle": int(os.getenv("MYSQL_POOL_RECYCLE", "1800")),
                "pool_pre_ping": True,
            }
        }

    db.init_app(app)


def get_db() -> SQLAlchemy:
    """获取 SQLAlchemy 实例。"""
    return db
