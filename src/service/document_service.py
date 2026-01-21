#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/20 16:08
@Author  : tianshiyang
@File    : document_service.py
"""
import os
from datetime import datetime

from config.db_config import db
from entities.dataset_entities import DatasetStatus
from entities.document_entities import DocumentStatus
from pkg.exception import FailException
from schema.document_schema import DocumentUploadToMilvusSchema
from model import Document
from service.dataset_service import update_dataset_status
from utils import get_module_logger
from task import add_document_to_milvus_task

# 使用统一的日志记录器
logger = get_module_logger(__name__)


def document_upload_service(req: DocumentUploadToMilvusSchema, user_id: str) -> Document:
    """文档上传，并同步上传Milvus做解析"""
    oss_url = req.oss_url.data
    dataset_id = req.dataset_id.data
    name = os.path.basename(oss_url)
    document = Document(
        dataset_id=dataset_id,
        user_id=user_id,
        oss_url=oss_url,
        name=name,
        status=DocumentStatus.PARSING.value,
        parsing_date=datetime.now(),
    )
    document.create()
    # 更新知识库状态
    update_dataset_status(
        dataset_id=dataset_id,
        user_id=user_id,
        status=DatasetStatus.PARING
    )
    # 开启异步任务解析文件
    print(str(document.id), oss_url, dataset_id, user_id)
    add_document_to_milvus_task.delay(oss_url=oss_url, dataset_id=dataset_id, user_id=user_id, document_id=str(document.id))
    return document

def get_document_detail(user_id: str, document_id: str) -> Document:
    """获取文档详情"""
    dataset = db.session.query(Document).filter(Document.id == document_id).first()
    if str(dataset.user_id) != user_id:
        raise FailException("知识库不存在")
    return dataset

def update_document_status(document_id: str, user_id: str, status: DocumentStatus, **kwargs):
    """更新文档状态"""
    document = get_document_detail(user_id=user_id, document_id=document_id)
    logger.error(f"kwarg: {kwargs}, 这个是kwarg")
    document.update(
        status=status.value,
        **kwargs
    )
    # 更新知识库状态 -> 不管成功或失败都让知识库完成
    update_dataset_status(
        dataset_id=str(document.dataset_id),
        user_id=user_id,
        status=DatasetStatus.USING,
    )
