#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/21 10:32
@Author  : tianshiyang
@File    : redis_config.py

Redis 配置：
- app.redis        通用 Redis 客户端（连接池复用）
- app.redis_stream 流式推送专用（独立连接池 / 可用不同 DB）
"""
import os

from flask import Flask
from redis import ConnectionPool, Redis


def _build_pool(host: str, port: int, db: int, password: str, max_connections: int) -> ConnectionPool:
    """构建 Redis 连接池。"""
    return ConnectionPool(
        host=host or "localhost",
        port=port,
        db=db,
        password=password or None,
        max_connections=max_connections,
        decode_responses=True,
    )


def init_redis_config(app: Flask) -> None:
    """初始化 Redis 连接池并绑定到 app.redis / app.redis_stream。"""
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    password = os.getenv("REDIS_PASSWORD", "").strip() or None

    # ── 通用 Redis ──
    pool = _build_pool(
        host=host,
        port=port,
        db=int(os.getenv("REDIS_DB", "0")),
        password=password,
        max_connections=int(os.getenv("REDIS_POOL_SIZE", "20")),
    )
    app.redis = Redis(connection_pool=pool)

    # ── 流式推送专用 Redis ──
    stream_pool = _build_pool(
        host=host,
        port=port,
        db=int(os.getenv("REDIS_STREAM_DB", "2")),
        password=password,
        max_connections=int(os.getenv("REDIS_STREAM_POOL_SIZE", "10")),
    )
    app.redis_stream = Redis(connection_pool=stream_pool)
