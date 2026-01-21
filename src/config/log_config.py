#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志配置模块 - 统一配置同步和异步日志
"""
import os
import logging
import logging.handlers
from flask import Flask


# 全局标记，避免重复初始化
_logging_configured = False

def log_config_init(app: Flask = None):
    # 配置参数
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_dir = os.getenv('LOG_DIR', 'logs')

    # 创建日志目录（使用绝对路径）
    log_dir = os.path.abspath(log_dir)
    os.makedirs(log_dir, exist_ok=True)

    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # 清除已有处理器（避免重复添加）
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    # 控制台处理器（同时输出到控制台和文件）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level, logging.INFO))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 文件处理器（所有日志都记录到一个文件）
    log_file = os.path.join(log_dir, 'app.log')
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8',
        delay=False
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Flask 日志配置
    if app:
        app.logger.setLevel(getattr(logging, log_level, logging.INFO))

    # 减少第三方库日志噪音
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    # 过滤 Celery 内部的 DEBUG 日志
    logging.getLogger('celery').setLevel(logging.INFO)  # Celery 主日志
    logging.getLogger('celery.utils.functional').setLevel(logging.WARNING)  # 过滤 functional 模块的 DEBUG
    logging.getLogger('celery.worker').setLevel(logging.INFO)  # Worker 日志
    logging.getLogger('celery.task').setLevel(logging.INFO)  # Task 日志


def init_log_config(app: Flask = None, force: bool = False):
    """
    初始化日志配置（统一配置，支持 Flask 和 Celery）
    
    环境变量:
    - LOG_LEVEL: 日志级别 (DEBUG/INFO/WARNING/ERROR/CRITICAL)，默认 INFO
    - LOG_DIR: 日志目录，默认 logs
    
    Args:
        app: Flask 应用实例（可选）
        force: 强制重新初始化（用于 Celery worker）
    """
    global _logging_configured
    
    if _logging_configured and not force:
        return

    log_config_init(app)


    _logging_configured = True


def get_logger(name: str) -> logging.Logger:
    """
    获取日志记录器（统一接口，支持同步和异步）
    
    Args:
        name: 模块名，通常使用 __name__
    
    Returns:
        logging.Logger: 日志记录器实例
    """
    # 如果未初始化，先初始化
    if not _logging_configured:
        init_log_config()
    
    logger = logging.getLogger(name)
    # 确保日志传播到根日志记录器
    logger.propagate = True
    # 确保日志记录器级别不会阻止日志
    if logger.level == logging.NOTSET:
        logger.setLevel(logging.DEBUG)
    
    return logger


# 提供统一的 logger 接口，可以直接使用 logging 模块的方法
def setup_logging():
    """
    设置统一的日志配置（用于直接使用 logging 模块的场景）
    """
    init_log_config()
