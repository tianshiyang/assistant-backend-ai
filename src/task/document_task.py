#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/20 18:29
@Author  : tianshiyang
@File    : document_task.py
"""
import time

from celery import shared_task

from utils import get_module_logger

# 获取日志记录器
logger = get_module_logger(__name__)


@shared_task
def add_document_to_milvus_task(user_id: str):
    """
    将文档添加到 Milvus 的异步任务
    
    Args:
        user_id: 用户ID
    """
    logger.info(f"开始执行任务: add_document_to_milvus_task, user_id={user_id}")
    
    try:
        # 模拟长时间任务（测试时可以改小，生产环境根据实际需求调整）
        # 4000 秒 = 约 66 分钟，用于测试时可以改为较小的值，如 10 秒
        time.sleep(10)


        logger.info(f"任务等待完成，继续执行后续逻辑，user_id={user_id}")
        logger.error(f"任务执行成功，user_id={user_id}")
        logger.error(f"定时任务celery，获取的user_id是{user_id}")
        
        # TODO: 在这里添加实际的业务逻辑
        # 例如：从 OSS 下载文件，解析文档，添加到 Milvus 等
        
        logger.info(f"任务完成，返回结果，user_id={user_id}")
        return {"status": "success", "user_id": user_id}
    except Exception as e:
        logger.error(f"任务执行失败，user_id={user_id}, 错误: {e}", exc_info=True)
        raise
