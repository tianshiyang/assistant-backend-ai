#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 16:30
@Author  : tianshiyang
@File    : message.py
"""
import uuid

from sqlalchemy import UUID, Integer, Text, VARCHAR, text
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

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="用户提问的问题",
    )

    messages: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=text("'[]'::jsonb"),
        comment="AI相应的内容（流式输出的每个chunk）",
    )

    answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=text(''),
        comment="AI回复的内容"
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

