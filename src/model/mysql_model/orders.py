#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/25 22:03
@Author  : tianshiyang
@File    : orders.py
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, BigInteger, Date, DateTime, Numeric, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TIMESTAMP
from datetime import datetime

from config.db_config import db
from model.base_model import BaseModel
from utils import format_time

if TYPE_CHECKING:
    from model.mysql_model import SalesPerson, Product, Customer


class Orders(BaseModel):
    __bind_key__ = 'mysql'
    __tablename__ = 'orders'
    __table_args__ = (
        Index("idx_order_date", "order_date"),
        Index("idx_user_date", "customer_id", "order_date"),
        Index("idx_sales_date", "sales_id", "order_date"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="主键ID"
    )

    order_no: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        comment="订单号"
    )

    customer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("customer.id"),
        nullable=False,
        comment="客户ID"
    )

    sales_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("sales_person.id"),
        nullable=True,
        comment="销售人员ID"
    )

    order_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=db.text("now()"),
        nullable=False,
        comment="下单日期"
    )

    order_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="created/paid/shipped/completed/canceled"
    )

    total_amount: Mapped[float] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable=False,
        comment="订单总金额"
    )

    paid_amount: Mapped[float] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable=False,
        default=0.00,
        comment="已支付金额"
    )

    sales: Mapped["SalesPerson"] = relationship(
        "SalesPerson",
        back_populates="orders"
    )

    customer: Mapped["Customer"] = relationship(
        "Customer",
        back_populates="orders"
    )

    order_item: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="orders"
    )

    def to_dict(self):
        """在基类字段基础上，额外返回分类名称"""
        data = super().to_dict()
        data["order_date"] = format_time(data["order_date"])
        data["sales_name"] = self.sales.name if self.sales else None
        data["customer_name"] = self.customer.name if self.customer else None
        data["order_item"] = [item.to_dict() for item in self.order_item] if self.order_item else []
        return data


class OrderItem(BaseModel):
    __bind_key__ = 'mysql'
    __tablename__ = 'order_item'
    __table_args__ = (
        Index("idx_order", "order_id"),
        Index("idx_product", "product_id"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="主键ID"
    )

    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("orders.id"),
        nullable=False,
        comment="订单ID"
    )

    product_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("product.id"),
        nullable=False,
        comment="商品ID",
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="购买数量"
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
        comment="成交单价"
    )

    total_price: Mapped[float] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable=False,
        comment="小计金额"
    )

    orders: Mapped["Orders"] = relationship(
        "Orders",
        back_populates="order_item"
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="order_item"
    )

    def to_dict(self):
        data = super().to_dict()
        data["product_name"] = self.product.name if self.product else None
        return data