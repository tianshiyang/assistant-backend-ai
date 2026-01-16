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

from sqlalchemy import UniqueConstraint, UUID, Text, String, VARCHAR, TIMESTAMP
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

    account_status: Mapped[str] = mapped_column(
        VARCHAR(10),
        nullable=False,
        comment="用户状态：using-使用中；logout-注销",
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

    # def __repr__(self) -> str:
    #     return f"<Account id={self.id} username={self.username}>"

# class User(BaseModel):
#     """
#     用户表模型
#     """
#     __tablename__ = 'users'
#
#     username = db.Column(db.String(32), unique=True, nullable=False, index=True, comment='用户名')
#     password_hash = db.Column(db.String(255), nullable=False, comment='密码哈希值')
#     email = db.Column(db.String(100), unique=True, nullable=True, comment='邮箱')
#     is_active = db.Column(db.Boolean, default=True, nullable=False, comment='是否激活')
#
#     def __repr__(self):
#         return f'<User {self.username}>'
#
#     @classmethod
#     def get_by_username(cls, username):
#         """根据用户名获取用户"""
#         return cls.query.filter_by(username=username).first()
#
#     @classmethod
#     def get_by_email(cls, email):
#         """根据邮箱获取用户"""
#         return cls.query.filter_by(email=email).first()
