#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/20 16:11
@Author  : tianshiyang
@File    : document.py
"""
import uuid
from datetime import datetime

from sqlalchemy import UUID, VARCHAR, Integer, TIMESTAMP, Text
from sqlalchemy.orm import Mapped, mapped_column

from config.db_config import db
from entities.document_entities import DocumentStatus
from model import BaseModel


class Document(BaseModel):
    __tablename__ = 'document'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="文档id"
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        comment="用户id"
    )

    dataset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        comment="知识库id"
    )

    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        comment="文档名称"
    )

    oss_url: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        comment="腾讯云oss_url"
    )

    character_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="文档字数"
    )

    token_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="文档token数"
    )

    parsing_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=db.text("now()"),
        comment="文档解析时间"
    )

    completed_date: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        comment="解析完成时间"
    )

    status: Mapped[str] = mapped_column(
        VARCHAR(10),
        nullable=False,
        default=DocumentStatus.PARSING.value,  # "parsing"
        comment="当前状态"
    )

    error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
        comment="错误原因"
    )