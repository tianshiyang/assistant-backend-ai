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
from pkg.exception import FailException
from schema.dataset_schema import CreateDatasetSchema, GetDataSetDetailSchema, UpdateDatasetSchema


def create_dataset_service(req: CreateDatasetSchema, user_id: str) -> Dataset:
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

def get_dataset_detail_by_id(dataset_id: str, user_id: str) -> Dataset:
    dataset = db.session.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.user_id == user_id
    ).first()
    return dataset

def get_dataset_detail_service(req: GetDataSetDetailSchema, user_id: str) -> Dataset:
    """获取知识库详情"""
    dataset_id = req.dataset_id.data
    dataset = get_dataset_detail_by_id(dataset_id, user_id)
    return dataset

def update_dataset_service(req: UpdateDatasetSchema, user_id: str) -> Dataset:
    """更新知识库"""
    dataset_id = req.dataset_id.data
    dataset = get_dataset_detail_by_id(dataset_id, user_id)
    if dataset is None:
        raise FailException("当前知识库不存在")
    print(dataset.id, '书库哈法')
    dataset.update(
        name=req.name.data,
        description=req.description.data,
        icon=req.icon.data,
    )
    return dataset