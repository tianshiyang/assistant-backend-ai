#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/25 22:22
@Author  : tianshiyang
@File    : order_service.py
"""
from sqlalchemy.orm import joinedload

from config.db_config import db
from entities.base_entity import Pagination
from model.mysql_model import Orders
from schema.order_schema import GetOrderListSchema


def get_order_list_service(req: GetOrderListSchema) -> Pagination[Orders]:
    """获取订单列表"""
    filters = []
    if req.order_no.data:
        filters.append(Orders.order_no == req.order_no.data)

    pagination = (
        db.session.query(Orders)
        .options(joinedload(Orders.order_item))  # 从根实体 Orders 预加载订单明细
        .filter(*filters)
        .order_by(Orders.created_at.desc())
        .paginate(
            page=int(req.page_no.data),
            per_page=int(req.page_size.data),
            error_out=False,
        )
    )

    return pagination