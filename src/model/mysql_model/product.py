#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/16
@Author  : tianshiyang
@File    : product.py
商品模型（对应表 product）
"""

from decimal import Decimal

from sqlalchemy import String, BigInteger, SmallInteger, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from model.base_model import BaseModel


class Product(BaseModel):
    __bind_key__ = "mysql"
    __tablename__ = "product"
    __table_args__ = (UniqueConstraint("product_no", name="product_no"),)

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="主键",
    )

    product_no: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="商品编号",
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="商品名称",
    )

    category_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="分类ID",
    )

    standard_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="标准售价",
    )

    cost_price: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
        comment="成本价",
    )

    status: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=1,
        comment="1=上架 0=下架",
    )

    deleted: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=0,
        comment="逻辑删除标志",
    )

