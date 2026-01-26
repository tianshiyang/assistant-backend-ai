#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/21 10:32
@Author  : tianshiyang
@File    : redis_config.py

Redis 配置与连接池：
- 通用 Redis：app.redis（连接池复用）
- 流式中断专用 Redis：app.redis_stream（独立连接池，可用不同 DB 或同实例不同 db index）
"""
import os

from flask import Flask
from redis import Redis
from redis.connection import ConnectionPool


def _parse_bool_env(key: str, default: bool = False) -> bool:
    return os.getenv(key, str(default)).lower() in ("1", "true", "yes")


def _build_pool(
    host: str,
    port: int,
    db: int,
    password: str | None,
    username: str | None,
    use_ssl: bool,
    max_connections: int = 20,
) -> ConnectionPool:
    return ConnectionPool(
        host=host or "localhost",
        port=port,
        db=db,
        password=password or None,
        username=username or None,
        ssl=use_ssl,
        max_connections=max_connections,
        decode_responses=True,
    )


def init_redis_config(app: Flask) -> None:
    """初始化 Redis 配置与连接池，并绑定到 app.redis / app.redis_stream。"""
    # 通用 Redis 配置（写进 app.config，兼容现有用法）
    app.config["REDIS_HOST"] = os.getenv("REDIS_HOST")
    app.config["REDIS_PORT"] = int(os.getenv("REDIS_PORT"))
    app.config["REDIS_USERNAME"] = os.getenv("REDIS_USERNAME")
    app.config["REDIS_PASSWORD"] = os.getenv("REDIS_PASSWORD")
    app.config["REDIS_DB"] = int(os.getenv("REDIS_DB", "0"))
    app.config["REDIS_USE_SSL"] = _parse_bool_env("REDIS_USE_SSL", False)
    app.config["REDIS_POOL_SIZE"] = int(os.getenv("REDIS_POOL_SIZE", "20"))

    # 通用 Redis 连接池 + 客户端
    pool = _build_pool(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        db=app.config["REDIS_DB"],
        password=app.config["REDIS_PASSWORD"],
        username=app.config["REDIS_USERNAME"],
        use_ssl=app.config["REDIS_USE_SSL"],
        max_connections=app.config["REDIS_POOL_SIZE"],
    )
    app.redis_pool = pool
    app.redis = Redis(connection_pool=pool)

    # 流式中断专用 Redis（可复用同实例不同 DB，或单独实例）
    stream_host = app.config["REDIS_HOST"]
    stream_port = int(app.config["REDIS_PORT"])
    stream_db = int(os.getenv("REDIS_STREAM_DB", "2"))
    stream_pool_size = int(os.getenv("REDIS_STREAM_POOL_SIZE", "10"))

    stream_pool = _build_pool(
        host=stream_host,
        port=stream_port,
        db=stream_db,
        password=os.getenv("REDIS_STREAM_PASSWORD") or app.config["REDIS_PASSWORD"],
        username=os.getenv("REDIS_STREAM_USERNAME") or app.config["REDIS_USERNAME"],
        use_ssl=_parse_bool_env("REDIS_STREAM_USE_SSL", app.config["REDIS_USE_SSL"]),
        max_connections=stream_pool_size,
    )
    app.redis_stream_pool = stream_pool
    app.redis_stream = Redis(connection_pool=stream_pool)