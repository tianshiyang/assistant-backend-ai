#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/20 16:08
@Author  : tianshiyang
@File    : document_service.py
"""
import os
from datetime import datetime

from entities.document_entities import DocumentStatus
from schema.document_schema import DocumentUploadToMilvusSchema
from model import Document
from utils import get_module_logger
from task import add_document_to_milvus_task

# 使用统一的日志记录器
logger = get_module_logger(__name__)


def document_upload_service(req: DocumentUploadToMilvusSchema, user_id: str) -> Document:
    """插入文档到milvus数据库中"""
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
    add_document_to_milvus_task.delay(user_id)
    return document