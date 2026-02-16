#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/16
@Author  : tianshiyang
@File    : customer_handler.py
"""
from flask import request
from flask_jwt_extended import jwt_required

from pkg.response import validate_error_json, success_json, success_message
from schema.customer_schema import (
    CreateCustomerSchema,
    UpdateCustomerSchema,
    GetCustomerDetailSchema,
    GetCustomerListSchema,
)
from service.customer_service import (
    create_customer_service,
    update_customer_service,
    get_customer_by_id_service,
    get_customer_list_service,
)
from utils import transform_pagination_data


@jwt_required()
def create_customer_handler():
    """新增客户"""
    req = CreateCustomerSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    custom = create_customer_service(req)
    return success_json(custom.to_dict())


@jwt_required()
def update_customer_handler():
    """编辑客户"""
    req = UpdateCustomerSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    customer = update_customer_service(req)
    return success_json(customer.to_dict())


@jwt_required()
def get_customer_list_handler():
    """查询客户列表"""
    req = GetCustomerListSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    pagination = get_customer_list_service(req)
    return success_json(transform_pagination_data(pagination))


@jwt_required()
def get_customer_detail_handler():
    """根据id查询客户详情"""
    req = GetCustomerDetailSchema(formdata=request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    customer = get_customer_by_id_service(req.customer_id.data)
    return success_json(customer.to_dict())
