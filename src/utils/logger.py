#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志工具模块
提供便捷的日志记录功能
"""
import logging
from typing import Optional

from ..config.log_config import get_logger


def get_module_logger(name: Optional[str] = None) -> logging.Logger:
    """
    获取模块日志记录器
    
    使用示例:
        from utils.logger import get_module_logger
        
        logger = get_module_logger(__name__)
        logger.info("这是一条信息日志")
        logger.error("这是一条错误日志")
    
    Args:
        name: 日志记录器名称，通常是 __name__
               如果不提供，将使用调用模块的名称
    
    Returns:
        logging.Logger: 日志记录器实例
    """
    if name is None:
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'unknown')
    
    return get_logger(name)
