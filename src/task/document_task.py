#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/20 18:29
@Author  : tianshiyang
@File    : document_task.py
"""
from datetime import datetime

from celery import shared_task

from entities.document_entities import DocumentStatus
from utils import get_module_logger

# 获取日志记录器
logger = get_module_logger(__name__)


@shared_task
def add_document_to_milvus_task(oss_url: str, dataset_id: str, document_id: str, user_id: str):
    """
    将文档添加到 Milvus 的异步任务
    
    Args:
        oss_url: 文件oss地址
        user_id: 用户ID
        document_id: 文档id
        dataset_id: 知识库id
    """
    from service.file_extractor_service import load_file_from_url
    from service.milvus_database_service import add_documents
    from service.document_service import update_document_status
    logger.info(f"开始：load_file_from_url")
    document_chunks, token_count, character_count = load_file_from_url(oss_url)
    logger.info(f"开始准备插入文档")
    try:
        """添加文档到milvus中"""
        add_documents(
            documents=document_chunks,
            user_id=user_id,
            document_id=document_id,
            dataset_id=dataset_id,
            source=oss_url
        )
        """更新文档状态为解析成功"""
        update_document_status(
            user_id=user_id,
            document_id=document_id,
            status=DocumentStatus.COMPLETED,
            token_count=token_count,
            character_count=character_count,
            completed_date=datetime.now()
        )
        logger.info(f"插入milvus成功")
    except Exception as e:
        """"更新文档状态为失败"""
        logger.error(f"更新文档失败：{e}")
        update_document_status(
            user_id=user_id,
            document_id=document_id,
            status=DocumentStatus.ERROR,
            error=str(e),
        )

@shared_task
def delete_document_to_milvus_task(user_id: str, document_id: str):
    """
    异步删除Milvus中的文档
    :param user_id: 用户id
    :param document_id: 文档id
    :return:
    """
    from service.milvus_database_service import delete_documents
    try:
        logger.info("==== 异步删除文档开始 ====")
        delete_documents(user_id=user_id, document_id=document_id)
    except Exception as e:
        logger.error(f"异步删除Milvus中的文档失败, 失败原因：{e}")



