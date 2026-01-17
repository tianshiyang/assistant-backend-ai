#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/17 23:03
@Author  : tianshiyang
@File    : dataset_service.py
"""
from uuid import UUID

from config.db_config import db
from model import Dataset
from schema.dataset_schema import CreateDatasetSchema, GetDataSetDetailSchema


def create_dataset_service(req: CreateDatasetSchema, user_id: UUID) -> Dataset:
    """创建知识库"""
    name = req.name.data
    icon = req.icon.data
    description = req.description.data
    dataset = Dataset(
        user_id=user_id,
        name=name,
        icon=icon,
        description=description
    ).create()
    return dataset

def get_dataset_detail_service(req: GetDataSetDetailSchema, user_id: UUID) -> Dataset:
    """获取知识库详情"""
    dataset_id = UUID(req.dataset_id.data)
    
    dataset = db.session.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.user_id == user_id
    ).first()
    
    return dataset