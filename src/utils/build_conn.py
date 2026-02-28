#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/27 17:05
@Author  : tianshiyang
@File    : build_conn.py
"""
import os


def build_mysql_uri() -> str:
    """从环境变量拼装 MySQL URI。"""
    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = os.getenv("MYSQL_PORT", "3306")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "")
    charset = os.getenv("MYSQL_CHARSET", "utf8mb4")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}"