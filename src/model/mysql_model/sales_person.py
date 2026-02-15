#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/15
@Author  : tianshiyang
@File    : sales_person.py
销售人员模型
"""

from sqlalchemy import String, Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from model.base_model import BaseModel


class SalesPerson(BaseModel):
    __bind_key__ = 'mysql'
    __tablename__ = 'sales_person'
    __table_args__ = (
        UniqueConstraint("sales_no", name="sales_no"),
        UniqueConstraint("assistant_id", name="uk_external_user"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="主键ID"
    )

    assistant_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="AI助手项目对应的用户id"
    )

    sales_no: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="销售人员编号"
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="销售人员名称"
    )

    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="销售人员邮箱"
    )

    phone: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="销售人员手机号"
    )

    status: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        comment="1=在职 0=离职"
    )

    is_deleted: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="逻辑删除标志"
    )