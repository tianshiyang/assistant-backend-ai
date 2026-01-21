#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
定时清理日志任务
"""
import os
from celery import shared_task
from utils import get_module_logger

logger = get_module_logger(__name__)


@shared_task
def cleanup_old_logs_task():
    """
    清理旧的日志文件（定时任务）
    """
    from config.log_config import clean_old_logs
    
    log_dir = os.getenv('LOG_DIR', 'logs')
    log_days_to_keep = int(os.getenv('LOG_DAYS_TO_KEEP', '5'))
    
    logger.info(f"开始清理 {log_dir} 目录中超过 {log_days_to_keep} 天的日志文件")
    clean_old_logs(log_dir, log_days_to_keep)
    logger.info("日志清理任务完成")
    
    return {"status": "success", "message": f"清理完成，保留 {log_days_to_keep} 天的日志"}
