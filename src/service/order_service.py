#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/25 22:22
@Author  : tianshiyang
@File    : order_service.py

多表预加载说明（避免 N+1）：
- 根实体是 Orders，列表里每条订单 to_dict() 会访问：order_item、sales、order_item[].product。
- 因此用 joinedload 一次预加载：Orders.order_item、Orders.sales、OrderItem.product（链式）。
"""
from sqlalchemy.orm import joinedload
from datetime import datetime
from config.db_config import db
from entities.base_entity import Pagination
from entities.order_entity import OrderStatus
from model.mysql_model import Orders, OrderItem
from pkg.exception import FailException
from schema.order_schema import GetOrderListSchema, CreateOrderSchema, PayOrderSchema, CancelPayOrderSchema, \
    DeleteOrderSchema
from service.product_service import get_product_detail_service


def _generate_order_no() -> str:
    """生成订单编号：O + 年月日(YYYYMMDD) + 当日顺序号(3位)，如 P20260225001。
    查询当日最后一个商品编号，在其基础上 +1；当日无商品则从 001 开始。
    """
    date_part = datetime.now().strftime("%Y%m%d")
    prefix = f"O{date_part}"

    last = (
        db.session.query(Orders)
        .filter(Orders.order_no.like(f"{prefix}%"))
        .order_by(Orders.order_no.desc())
        .first()
    )

    if last is None:
        seq = 1
    else:
        try:
            # 取编号后 3 位为顺序号
            seq = int(last.order_no[-3:]) + 1
        except (ValueError, IndexError):
            seq = 1
    if seq > 999:
        raise FailException("当日新增订单已达上限，请明日再试")
    return f"{prefix}{str(seq).zfill(3)}"


def get_order_list_service(req: GetOrderListSchema) -> Pagination[Orders]:
    """获取订单列表"""
    filters = []
    if req.order_no.data:
        filters.append(Orders.order_no == req.order_no.data)

    pagination = (
        db.session.query(Orders)
        .options(
            joinedload(Orders.order_item).joinedload(OrderItem.product),  # 订单明细 + 商品
            joinedload(Orders.sales),  # 销售人员（to_dict 里 sales_name）
        )
        .filter(*filters)
        .order_by(Orders.created_at.desc())
        .paginate(
            page=int(req.page_no.data),
            per_page=int(req.page_size.data),
            error_out=False,
        )
    )

    return pagination

def create_order_service(req: CreateOrderSchema) -> Orders:
    """创建订单"""
    product = get_product_detail_service(req.product_id.data)
    sales_id = req.sales_id.data
    customer_id = req.customer_id.data
    product_id = req.product_id.data
    quantity = req.quantity.data
    unit_price = product.standard_price
    order_no = _generate_order_no()

    order = Orders(
        order_no=order_no,
        sales_id=sales_id,
        customer_id=customer_id,
        order_date=datetime.now(),
        order_status=OrderStatus.CREATED.value,
        total_amount=quantity * unit_price,
        paid_amount=0,
    )

    order_item = OrderItem(
        orders=order,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        total_price=quantity * unit_price,
    )

    try:
        db.session.add(order)
        db.session.add(order_item)
        db.session.commit()   # 一次提交，订单+明细要么都成功，要么都失败
    except Exception:
        db.session.rollback()
        raise
    return order

def get_order_detail_service(order_id: int) -> Orders:
    order = db.session.query(Orders).filter(Orders.id == order_id).first()
    if order is None:
        raise FailException("订单不存在")
    return order

def pay_order_service(req: PayOrderSchema) -> Orders:
    """支付订单"""
    order_id = req.order_id.data
    order = get_order_detail_service(order_id)
    paid_amount = order.paid_amount
    remaining_amount = order.total_amount - paid_amount
    pay_amount = req.pay_amount.data
    if remaining_amount < pay_amount:
        raise FailException("支付金额大于剩余金额")

    if remaining_amount == pay_amount:
        # 支付完成
        order.update(
            paid_amount=order.paid_amount + pay_amount,
            order_status=OrderStatus.COMPLETED.value,
        )
    if remaining_amount > pay_amount:
        # 支付中
        order.update(
            paid_amount=order.paid_amount + pay_amount,
            order_status=OrderStatus.PAID.value,
        )
    return order

def cancel_pay_order_service(req: CancelPayOrderSchema) -> Orders:
    """取消订单"""
    order_id = req.order_id.data
    order = get_order_detail_service(order_id)
    order.update(order_status=OrderStatus.CANCELED.value)
    return order

def delete_order_service(req: DeleteOrderSchema) -> Orders:
    order_id = req.order_id.data
    order = get_order_detail_service(order_id)
    db.session.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
    order.delete()
    return order
