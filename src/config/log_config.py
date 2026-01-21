#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志配置模块 - 统一配置同步和异步日志
支持按日期分类，自动清理旧日志
"""
import os
import logging
import logging.handlers
import glob
from datetime import datetime, timedelta
from flask import Flask


# 全局标记，避免重复初始化
_logging_configured = False


def clean_old_logs(log_dir: str, days_to_keep: int = 5):
    """
    清理旧的日志文件
    
    Args:
        log_dir: 日志目录
        days_to_keep: 保留天数，默认5天
    """
    try:
        # 计算截止日期
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # 查找所有日志文件（app.log 和 app.log.YYYY-MM-DD）
        log_pattern = os.path.join(log_dir, 'app.log*')
        log_files = glob.glob(log_pattern)
        
        deleted_count = 0
        for log_file in log_files:
            try:
                # 获取文件修改时间
                file_mtime = datetime.fromtimestamp(os.path.getmtime(log_file))
                
                # 如果文件超过保留天数，删除
                if file_mtime < cutoff_date:
                    os.remove(log_file)
                    deleted_count += 1
            except Exception:
                # 忽略删除失败的文件
                pass
        
        if deleted_count > 0:
            logging.getLogger().info(f"清理了 {deleted_count} 个旧日志文件")
    except Exception as e:
        logging.getLogger().warning(f"清理旧日志文件时出错: {e}")


def log_config_init(app: Flask = None):
    """
    初始化日志配置
    
    Args:
        app: Flask 应用实例（可选）
    """
    # 配置参数
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_dir = os.getenv('LOG_DIR', 'logs')
    log_max_bytes = int(os.getenv('LOG_MAX_BYTES', '2097152'))  # 2MB
    log_days_to_keep = int(os.getenv('LOG_DAYS_TO_KEEP', '5'))  # 保留5天
    
    # 创建日志目录（使用绝对路径）
    log_dir = os.path.abspath(log_dir)
    os.makedirs(log_dir, exist_ok=True)
    
    # 清理旧日志
    clean_old_logs(log_dir, log_days_to_keep)
    
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
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level, logging.INFO))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 文件处理器（按日期轮转，每天一个文件，同时限制文件大小）
    log_file = os.path.join(log_dir, 'app.log')
    
    try:
        # 使用 TimedRotatingFileHandler 按日期轮转
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_file,
            when='midnight',  # 每天午夜轮转
            interval=1,  # 每天
            backupCount=log_days_to_keep,  # 保留5天
            encoding='utf-8',
            delay=False
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        file_handler.suffix = '%Y-%m-%d'  # 日志文件后缀格式：app.log.2026-01-21
        
        # 限制单个文件大小（通过自定义 shouldRollover）
        original_should_rollover = file_handler.shouldRollover
        
        def should_rollover(record):
            # 检查是否需要按日期轮转
            if original_should_rollover(record):
                return True
            # 检查是否需要按大小轮转
            if file_handler.stream and hasattr(file_handler.stream, 'tell'):
                try:
                    msg = file_handler.format(record)
                    file_handler.stream.seek(0, 2)  # 移动到文件末尾
                    current_size = file_handler.stream.tell()
                    msg_size = len(msg.encode('utf-8'))
                    if current_size + msg_size >= log_max_bytes:
                        return True
                except (AttributeError, OSError):
                    pass
            return False
        
        file_handler.shouldRollover = should_rollover
        
        root_logger.addHandler(file_handler)
        root_logger.info(f"日志系统初始化完成，日志文件: {log_file}，保留 {log_days_to_keep} 天，单文件最大 {log_max_bytes // 1024 // 1024}MB")
    except Exception as e:
        root_logger.warning(f"无法创建日志文件 {log_file}: {e}")
    
    # Flask 日志配置
    if app:
        app.logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # 减少第三方库日志噪音
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    # 过滤 Celery 内部的 DEBUG 日志
    logging.getLogger('celery').setLevel(logging.INFO)
    logging.getLogger('celery.utils.functional').setLevel(logging.WARNING)
    logging.getLogger('celery.worker').setLevel(logging.INFO)
    logging.getLogger('celery.task').setLevel(logging.INFO)


def init_log_config(app: Flask = None, force: bool = False):
    """
    初始化日志配置（统一配置，支持 Flask 和 Celery）
    
    环境变量:
    - LOG_LEVEL: 日志级别 (DEBUG/INFO/WARNING/ERROR/CRITICAL)，默认 INFO
    - LOG_DIR: 日志目录，默认 logs
    - LOG_MAX_BYTES: 单个日志文件最大大小（字节），默认 2MB (2097152)
    - LOG_DAYS_TO_KEEP: 保留日志天数，默认 5 天
    
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


def setup_logging():
    """
    设置统一的日志配置（用于直接使用 logging 模块的场景）
    """
    init_log_config()
