#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 16:03
@Author  : tianshiyang
@File    : conversation.py
"""
import uuid

from sqlalchemy import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from model import BaseModel


class Conversation(BaseModel):
    __tablename__ = "conversation"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="会话ID",
    )

    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        default="新会话",
        comment="会话名称",
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        comment="用户id",
    )