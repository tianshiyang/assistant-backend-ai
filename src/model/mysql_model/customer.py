#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/16
@Author  : tianshiyang
@File    : customer_router.py
客户模型（与表 customer 一致）
"""

from sqlalchemy import String, BigInteger, SmallInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from model.base_model import BaseModel


class Customer(BaseModel):
    __bind_key__ = "mysql"
    __tablename__ = "customer"
    __table_args__ = (UniqueConstraint("user_no", name="user_no"),)

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="主键",
    )

    user_no: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="客户业务编号",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="客户姓名",
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="客户邮箱",
    )

    phone: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        comment="客户手机号",
    )

    status: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=1,
        comment="1=正常 0=禁用",
    )

    deleted: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=0,
        comment="软删除标识",
    )
