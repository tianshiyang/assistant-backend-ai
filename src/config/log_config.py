#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志配置模块 - 简化版
"""
import os
import logging
import logging.handlers
from flask import Flask

# 标记是否已初始化
_initialized = False


def init_log_config(app: Flask = None):
    """
    初始化日志配置（简单版本）
    
    环境变量（可选）:
    - LOG_LEVEL: 日志级别，默认 INFO
    - LOG_DIR: 日志目录，默认 logs
    """
    global _initialized
    
    # 避免重复初始化
    if _initialized:
        return
    
    # 获取配置
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_dir = os.getenv('LOG_DIR', 'logs')
    
    # 创建日志目录
    os.makedirs(log_dir, exist_ok=True)
    
    # 日志格式
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()  # 清除已有处理器
    
    # 控制台输出
    console = logging.StreamHandler()
    console.setLevel(getattr(logging, log_level, logging.INFO))
    console.setFormatter(log_format)
    root_logger.addHandler(console)
    
    # 文件输出（所有日志）
    log_file = os.path.join(log_dir, 'app.log')
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    # Flask 日志
    if app:
        app.logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # 减少第三方库日志噪音
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    _initialized = True


def get_logger(name: str) -> logging.Logger:
    """
    获取日志记录器（自动初始化）
    
    Args:
        name: 模块名，通常用 __name__
    
    Returns:
        logging.Logger: 日志记录器
    """
    if not _initialized:
        init_log_config()
    
    logger = logging.getLogger(name)
    logger.propagate = True  # 传播到根日志记录器
    return logger
