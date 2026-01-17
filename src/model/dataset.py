#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/17 21:21
@Author  : tianshiyang
@File    : dataset.py
"""
import uuid

from sqlalchemy import UUID, Text, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from entities.dataset_entities import DatasetStatus
from model import BaseModel

class Dataset(BaseModel):
    __tablename__ = "dataset"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="用户id"
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        comment="知识库关联的用户id"
    )

    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="知识库名称"
    )

    status: Mapped[str] = mapped_column(
        VARCHAR(10),
        nullable=False,
        default=DatasetStatus.USING,
        comment="知识库状态: parsing文件解析中 -> 不可选择此数据库，using -> 使用中"
    )

    icon: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
        comment="知识库icon图标"
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="知识库描述",
    )