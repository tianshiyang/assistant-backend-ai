#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13
@Author  : tianshiyang
@File    : account.py
用户模型
"""
import uuid
from datetime import datetime

from sqlalchemy import UniqueConstraint, UUID, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from model.base_model import BaseModel
from config.db_config import db

class Account(BaseModel):
    __tablename__ = 'account'
    __table_args__ = (
        UniqueConstraint("username", name="uq_account_username"),
        UniqueConstraint("email", name="uq_account_email"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="用户id"
    )

    username: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="用户邮箱"
    )

    email: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="用户邮箱",
    )

    avatar_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="用户头像"
    )

    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="加密后的用户密码"
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=db.text("now()"),
        comment="创建时间"
    )

    update_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=db.text("now()"),
        comment="更新时间",
    )
