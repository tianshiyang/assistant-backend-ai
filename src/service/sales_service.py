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
from schema.sales_schema import GetSalesByIdSchema, GetAllSalesSchema, UpdateSalesSchema


def get_sales_by_id_service(sales_id: int) -> SalesPerson:
    """通过销售id获取销售详情"""
    sales = db.session.query(SalesPerson).filter(SalesPerson.id == sales_id).first()
    if sales is None:
        raise FailException("无此销售")
    return sales

def get_all_sales_service(req: GetAllSalesSchema):
    """获取全部销售"""
    filters = []
    if req.sales_name.data:
        filters.append(SalesPerson.name.ilike(f'%{req.sales_name.data}%'))

    pagination = db.session.query(SalesPerson).filter(*filters).order_by(SalesPerson.created_at.desc()).paginate(
        page=int(req.page_no.data),
        per_page=int(req.page_size.data),
        error_out=False
    )
    return pagination

def update_sales_service(req: UpdateSalesSchema):
    """更新销售信息"""
    per_sales = get_sales_by_id_service(req.sales_id.data)
    if per_sales is None:
        raise FailException("找不到销售")

    update_data = {}
    if req.name.data:
        update_data['name'] = req.name.data
    if req.email.data:
        update_data['email'] = req.email.data
    if req.phone.data:
        update_data['phone'] = req.phone.data

    sales = per_sales.update(**update_data)
    return sales
