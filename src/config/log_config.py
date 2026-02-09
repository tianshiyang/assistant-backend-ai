#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志配置模块
"""
import os
import glob
import logging
import logging.handlers
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask

# ─── 常量 ────────────────────────────────────────────────────────
# 项目根目录（app.py 所在目录）
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_LOG_DIR = _PROJECT_ROOT / "logs"

# 全局标记，避免重复初始化
_logging_configured = False

# ─── 日志格式 ────────────────────────────────────────────────────
_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(filename)s:%(lineno)d - %(message)s"
_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ─── 清理旧日志 ──────────────────────────────────────────────────
def clean_old_logs(log_dir: str = None, days_to_keep: int = 7):
    """
    清理超过 days_to_keep 天的旧日志文件。
    """
    log_dir = log_dir or str(_LOG_DIR)
    cutoff = datetime.now() - timedelta(days=days_to_keep)

    for f in glob.glob(os.path.join(log_dir, "app.log.*")):
        try:
            if datetime.fromtimestamp(os.path.getmtime(f)) < cutoff:
                os.remove(f)
        except OSError:
            pass


# ─── 核心初始化 ──────────────────────────────────────────────────
def _setup_logging(app: Flask = None):
    """实际执行一次的日志配置。"""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    days_to_keep = int(os.getenv("LOG_DAYS_TO_KEEP", "7"))

    # 确保日志目录存在
    os.makedirs(_LOG_DIR, exist_ok=True)

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_LOG_DATE_FORMAT)

    effective_level = getattr(logging, log_level, logging.INFO)

    # ── root logger ──
    root = logging.getLogger()
    root.setLevel(effective_level)

    # 清除已有 handler（防止多次添加）
    for h in root.handlers[:]:
        root.removeHandler(h)
        h.close()

    # 控制台
    console = logging.StreamHandler()
    console.setLevel(effective_level)
    console.setFormatter(formatter)
    root.addHandler(console)

    # 文件（按日期轮转）—— 级别与 LOG_LEVEL 一致（生产默认 INFO）
    log_file = os.path.join(_LOG_DIR, "app.log")
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=days_to_keep,
        encoding="utf-8",
    )
    file_handler.suffix = "%Y-%m-%d"          # app.log.2026-02-09
    file_handler.setLevel(effective_level)
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    # 启动时清理过期日志
    clean_old_logs(str(_LOG_DIR), days_to_keep)

    # ── Flask logger ──
    if app:
        app.logger.setLevel(effective_level)

    # ── 降低第三方库日志噪音 ──
    for name in ("werkzeug", "urllib3", "requests"):
        logging.getLogger(name).setLevel(logging.WARNING)
    for name in ("celery", "celery.worker", "celery.task"):
        logging.getLogger(name).setLevel(logging.INFO)
    logging.getLogger("celery.utils.functional").setLevel(logging.WARNING)


# ─── 对外接口 ────────────────────────────────────────────────────
def init_log_config(app: Flask = None, force: bool = False):
    """
    初始化日志配置（Flask 启动 / Celery worker 启动时各调用一次）。

    环境变量：
        LOG_LEVEL       日志级别，默认 INFO
        LOG_DAYS_TO_KEEP 保留天数，默认 7
    """
    global _logging_configured
    if _logging_configured and not force:
        return
    _setup_logging(app)
    _logging_configured = True


def get_logger(name: str) -> logging.Logger:
    """获取模块级 logger（传 __name__ 即可）。"""
    if not _logging_configured:
        init_log_config()
    return logging.getLogger(name)
