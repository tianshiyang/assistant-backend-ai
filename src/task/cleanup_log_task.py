#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""定时清理日志任务"""
import os
from celery import shared_task
from utils import get_module_logger

logger = get_module_logger(__name__)


@shared_task
def cleanup_old_logs_task():
    """清理过期日志文件（由 Celery Beat 定时触发）。"""
    from config.log_config import clean_old_logs

    days = int(os.getenv("LOG_DAYS_TO_KEEP", "7"))
    logger.info(f"开始清理超过 {days} 天的旧日志文件")
    clean_old_logs(days_to_keep=days)
    logger.info("日志清理任务完成")
    return {"status": "success", "days_to_keep": days}
