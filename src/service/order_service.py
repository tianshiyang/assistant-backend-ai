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

from config.db_config import db
from entities.base_entity import Pagination
from model.mysql_model import Orders, OrderItem
from schema.order_schema import GetOrderListSchema


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