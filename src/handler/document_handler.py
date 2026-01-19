#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/19 22:03
@Author  : tianshiyang
@File    : document_handler.py
"""
from pkg.response import success_message
from service.milvus_database_service import add_documents


def document_upload_to_milvus_handler():
    add_documents()
    return success_message("插入成功")