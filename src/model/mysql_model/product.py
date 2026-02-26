#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/16
@Author  : tianshiyang
@File    : product_router.py
商品模型（对应表 product）
"""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger, SmallInteger, Numeric, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from model.base_model import BaseModel

if TYPE_CHECKING:
    from model.mysql_model import OrderItem

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

    # 反向关系：一个分类下有多个商品
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
    )


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
        ForeignKey("product_category.id"),
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

    category: Mapped[ProductCategory] = relationship(
        "ProductCategory",
        back_populates="products",
    )

    order_item: Mapped["OrderItem"] = relationship(
        "OrderItem",
        back_populates="product"
    )

    def to_dict(self):
        """在基类字段基础上，额外返回分类名称"""
        data = super().to_dict()
        data["category_name"] = self.category.category_name if self.category else None
        return data

