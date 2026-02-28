#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志工具模块：提供 get_module_logger，不依赖 config，避免循环导入。
应用启动时由 config.log_config.init_log_config() 配置 root logger，
此处仅返回 logging.getLogger(name)。
"""
import logging
from typing import Optional


def get_module_logger(name: Optional[str] = None) -> logging.Logger:
    """
    获取模块日志记录器（标准库 Logger，由 init_log_config 在应用启动时统一配置）。

    使用示例:
        from utils.logger import get_module_logger
        logger = get_module_logger(__name__)
    """
    if name is None:
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get("__name__", "unknown")
    return logging.getLogger(name)
