#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13
@Author  : tianshiyang
@File    : db_config.py
数据库配置
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# 创建 SQLAlchemy 实例
db = SQLAlchemy()


def init_db_config(app: Flask):
    """初始化数据库配置与 Postgres 连接池。"""
    database_url = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 连接池：pool_size 常驻连接数，max_overflow 额外可创建的连接数，pool_recycle 连接回收时间（秒）
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_size": int(os.getenv("SQLALCHEMY_POOL_SIZE", "5")),
        "max_overflow": int(os.getenv("SQLALCHEMY_MAX_OVERFLOW", "10")),
        "pool_recycle": int(os.getenv("SQLALCHEMY_POOL_RECYCLE", "3600")),
    }

    app.config['SQLALCHEMY_ECHO'] = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'  # 是否打印 SQL 语句
    
    # 初始化数据库
    db.init_app(app)
    
    # # 在应用上下文中创建表（可选，生产环境建议使用迁移工具）
    # with app.app_context():
    #     # 延迟导入模型，避免循环导入
    #     try:
    #         from model import BaseModel, User  # 这会触发模型注册
    #
    #         # 如果需要自动创建表（仅用于开发环境）
    #         if os.getenv('AUTO_CREATE_TABLES', 'False').lower() == 'true':
    #             db.create_all()
    #     except ImportError:
    #         # 如果模型还未定义，跳过
    #         pass


def get_db():
    """获取数据库实例"""
    return db
