#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/20 18:29
@Author  : tianshiyang
@File    : document_task.py
"""
import time

from celery import shared_task


@shared_task
def add_document_to_milvus_task(user_id: str):
    time.sleep(4000)
    print(user_id, '延迟任务user_id')
