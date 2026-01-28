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
    password: str,
    max_connections: int = 20,
) -> ConnectionPool:
    """构建 Redis 连接池（仅使用 password 认证）"""
    # ConnectionPool 不支持 ssl 参数，SSL 配置在 Redis 客户端层面处理
    pool_kwargs = {
        "host": host or "localhost",
        "port": port,
        "db": db,
        "max_connections": max_connections,
        "decode_responses": True,
        "password": password,
    }
    
    return ConnectionPool(**pool_kwargs)


def init_redis_config(app: Flask) -> None:
    """
    初始化 Redis 配置与连接池，并绑定到 app.redis / app.redis_stream。
    """
    # 通用 Redis 配置
    app.config["REDIS_HOST"] = os.getenv("REDIS_HOST", "localhost")
    app.config["REDIS_PORT"] = int(os.getenv("REDIS_PORT", "6379"))
    redis_password = os.getenv("REDIS_PASSWORD", "").strip()
    app.config["REDIS_PASSWORD"] = redis_password if redis_password else None
    app.config["REDIS_DB"] = int(os.getenv("REDIS_DB", "0"))
    app.config["REDIS_POOL_SIZE"] = int(os.getenv("REDIS_POOL_SIZE", "20"))

    # 通用 Redis 连接池 + 客户端
    pool = _build_pool(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        db=app.config["REDIS_DB"],
        password=app.config["REDIS_PASSWORD"],
        max_connections=app.config["REDIS_POOL_SIZE"],
    )
    app.redis_pool = pool
    redis_kwargs = {"connection_pool": pool}
    app.redis = Redis(**redis_kwargs)

    # 流式中断专用 Redis（可复用同实例不同 DB，或单独实例）
    stream_host = app.config["REDIS_HOST"]
    stream_port = int(app.config["REDIS_PORT"])
    stream_db = int(os.getenv("REDIS_STREAM_DB", "2"))
    stream_pool_size = int(os.getenv("REDIS_STREAM_POOL_SIZE", "10"))

    stream_password = app.config["REDIS_PASSWORD"]
    
    stream_pool = _build_pool(
        host=stream_host,
        port=stream_port,
        db=stream_db,
        password=stream_password,
        max_connections=stream_pool_size,
    )
    app.redis_stream_pool = stream_pool
    stream_redis_kwargs = {"connection_pool": stream_pool}
    app.redis_stream = Redis(**stream_redis_kwargs)