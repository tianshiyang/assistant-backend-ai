#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/22 18:21
@Author  : tianshiyang
@File    : dataset_task.py
"""
from celery import shared_task

from utils import get_module_logger

# 获取日志记录器
logger = get_module_logger(__name__)

@shared_task
def delete_dataset_to_milvus_documents_task(dataset_id: str, user_id: str):
    """删除知识库的时候，同步删除milvus中的数据
    :param dataset_id: 知识库id
    :param user_id: 用户id
    :return:
    """
    from service.milvus_database_service import delete_documents
    from service.document_service import delete_all_document_by_dataset_id
    try:
        logger.info("==== 异步删除文档开始 ====")
        delete_all_document_by_dataset_id(dataset_id, user_id)
        delete_documents(
            user_id=user_id,
            dataset_id=dataset_id,
        )
    except Exception as e:
        logger.error(f"删除知识库同步删除milvus中的document失败，失败原因{e}")