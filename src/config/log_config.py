#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志配置模块
"""
import os
import logging
import logging.handlers
from datetime import datetime
from flask import Flask


def init_log_config(app: Flask):
    """
    初始化日志配置
    
    环境变量:
    - LOG_LEVEL: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)，默认 INFO
    - LOG_DIR: 日志文件目录，默认 logs
    - LOG_MAX_BYTES: 单个日志文件最大字节数，默认 10MB
    - LOG_BACKUP_COUNT: 保留的日志文件数量，默认 10
    """
    # 获取日志配置
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_dir = os.getenv('LOG_DIR', 'logs')
    log_max_bytes = int(os.getenv('LOG_MAX_BYTES', '10485760'))  # 10MB
    log_backup_count = int(os.getenv('LOG_BACKUP_COUNT', '10'))
    
    # 创建日志目录
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 配置日志格式
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 获取根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # 清除已有的处理器
    root_logger.handlers.clear()
    
    # 控制台处理器（输出到终端）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level, logging.INFO))
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # 文件处理器 - 所有日志
    all_log_file = os.path.join(log_dir, 'app.log')
    file_handler = logging.handlers.RotatingFileHandler(
        all_log_file,
        maxBytes=log_max_bytes,
        backupCount=log_backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)  # 文件记录所有级别的日志
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    # 错误日志文件处理器 - 只记录 ERROR 及以上级别
    error_log_file = os.path.join(log_dir, 'error.log')
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=log_max_bytes,
        backupCount=log_backup_count,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)
    root_logger.addHandler(error_handler)
    
    # 配置 Flask 日志
    app.logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # 配置第三方库的日志级别
    logging.getLogger('werkzeug').setLevel(logging.WARNING)  # Flask 内部日志
    logging.getLogger('urllib3').setLevel(logging.WARNING)  # HTTP 库日志
    logging.getLogger('requests').setLevel(logging.WARNING)  # Requests 库日志
    
    # 记录启动信息
    app.logger.info('=' * 60)
    app.logger.info(f'应用启动 - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    app.logger.info(f'日志级别: {log_level}')
    app.logger.info(f'日志目录: {log_dir}')
    app.logger.info('=' * 60)


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的日志记录器
    
    Args:
        name: 日志记录器名称，通常是模块名 __name__
    
    Returns:
        logging.Logger: 日志记录器实例
    """
    return logging.getLogger(name)
