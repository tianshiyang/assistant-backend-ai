#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/16
@Author  : tianshiyang
@File    : product_category.py
商品分类模型（对应表 product_category）
"""

from sqlalchemy import String, BigInteger, SmallInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from model.base_model import BaseModel


class ProductCategory(BaseModel):
    __bind_key__ = "mysql"
    __tablename__ = "product_category"
    __table_args__ = (UniqueConstraint("category_code", name="category_code"),)

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="主键",
    )

    category_code: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="分类code",
    )

    category_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="分类名称",
    )

    status: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=1,
        comment="状态：1=启用 0=禁用",
    )

