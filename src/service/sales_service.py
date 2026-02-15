#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/15 18:28
@Author  : tianshiyang
@File    : sales_service.py
"""
from config.db_config import db
from model.mysql_model.sales_person import SalesPerson
from pkg.exception import FailException
from schema.sales_schema import GetSalesByIdSchema, GetAllSalesSchema


def get_sales_by_id_service(req: GetSalesByIdSchema):
    """通过销售id获取销售详情"""
    sales = db.session.query(SalesPerson).filter(SalesPerson.id == req.sales_id.data).first()
    if sales is None:
        raise FailException("无此销售")
    return sales

def get_all_sales_service(req: GetAllSalesSchema):
    """获取全部销售"""
    filters = []
    if req.sales_name.data:
        filters.append(SalesPerson.name.ilike(f'%{req.sales_name.data}%'))

    print(f"过滤条件{filters}")

    pagination = db.session.query(SalesPerson).filter(*filters).order_by(SalesPerson.created_at.desc()).paginate(
        page=int(req.page_no.data),
        per_page=int(req.page_size.data),
        error_out=False
    )
    return pagination
