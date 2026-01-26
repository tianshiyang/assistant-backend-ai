#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 16:30
@Author  : tianshiyang
@File    : message.py
"""
import uuid

from sqlalchemy import UUID, Integer, Text, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from model import BaseModel


class Message(BaseModel):
    __tablename__ = "message"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="消息id",
    )

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        comment="会话id",
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        comment="用户id",
    )

    query: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="用户提问的问题",
    )

    type: Mapped[str] = mapped_column(
        VARCHAR(10),
        nullable=False,
        comment="AI返回消息类型: ping-保持连通, done-完成, error-失败, tool-调用工具, generate-生成内容",
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
        comment="AI返回的内容",
    )

    input_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="输入token数量",
    )

    output_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="输出token数量",
    )

    total_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="总token数量",
    )

