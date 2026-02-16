#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/16
@Author  : tianshiyang
@File    : customer_service.py
"""
from datetime import datetime

from config.db_config import db
from model.mysql_model.customer import Customer
from pkg.exception import FailException
from schema.customer_schema import (
    CreateCustomerSchema,
    UpdateCustomerSchema,
    GetCustomerListSchema,
)


def _generate_user_no() -> str:
    """生成客户业务编号：U + 年月日(YYYYMMDD) + 当日顺序号(3位)，如 U20260203003。
    查询当日最后一个客户编号，在其基础上 +1；当日无客户则从 001 开始。
    """
    date_part = datetime.now().strftime("%Y%m%d")
    prefix = f"U{date_part}"

    last = (
        db.session.query(Customer)
        .filter(Customer.user_no.like(f"{prefix}%"), Customer.deleted == 0)
        .order_by(Customer.user_no.desc())
        .first()
    )

    if last is None:
        seq = 1
    else:
        try:
            # 取编号后 3 位为顺序号
            seq = int(last.user_no[-3:]) + 1
        except (ValueError, IndexError):
            seq = 1
    if seq > 999:
        raise FailException("当日客户编号已达上限，请明日再试")
    return f"{prefix}{str(seq).zfill(3)}"


def get_customer_by_id_service(customer_id: int) -> Customer:
    """根据id获取客户详情"""
    customer = (
        db.session.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.deleted == 0
        )
        .first()
    )
    if customer is None:
        raise FailException("客户不存在")
    return customer


def create_customer_service(req: CreateCustomerSchema) -> Customer:
    """新增客户（user_no 后端自动生成：查询当日最后编号 +1）"""
    user_no = _generate_user_no()
    customer = Customer(
        user_no=user_no,
        name=req.name.data,
        email=req.email.data or None,
        phone=req.phone.data or None,
        status=req.status.data if req.status.data is not None else 1,
    )
    return customer.create()


def update_customer_service(req: UpdateCustomerSchema) -> Customer:
    """编辑客户"""
    customer = get_customer_by_id_service(req.customer_id.data)
    update_data = {}
    if req.name.data is not None:
        update_data["name"] = req.name.data
    if req.email.data is not None:
        update_data["email"] = req.email.data
    if req.phone.data is not None:
        update_data["phone"] = req.phone.data
    if req.status.data is not None:
        update_data["status"] = req.status.data
    if update_data:
        customer.update(**update_data)
    return customer


def get_customer_list_service(req: GetCustomerListSchema):
    """查询客户列表（分页）"""
    filters = [Customer.deleted == 0]
    if req.user_no.data:
        filters.append(Customer.user_no == req.user_no.data)
    if req.name.data:
        filters.append(Customer.name.ilike(f"%{req.name.data}%"))
    if req.phone.data:
        filters.append(Customer.phone == req.phone.data)
    if req.status.data is not None:
        filters.append(Customer.status == req.status.data)

    pagination = (
        db.session.query(Customer)
        .filter(*filters)
        .order_by(Customer.created_at.desc())
        .paginate(
            page=int(req.page_no.data),
            per_page=int(req.page_size.data),
            error_out=False,
        )
    )
    return pagination
