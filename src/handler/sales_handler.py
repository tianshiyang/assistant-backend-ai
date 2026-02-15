#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/15 18:22
@Author  : tianshiyang
@File    : sales_handler.py
"""
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from pkg.response import validate_error_json, success_json
from schema.sales_schema import GetSalesByIdSchema, GetAllSalesSchema, UpdateSalesSchema
from service.sales_service import get_sales_by_id_service, get_all_sales_service, update_sales_service
from utils import transform_pagination_data


@jwt_required()
def get_sales_by_id_handler():
    """通过id获取销售详情"""
    req = GetSalesByIdSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)

    sales = get_sales_by_id_service(req.sales_id.data)
    return success_json(sales.to_dict())

@jwt_required()
def get_all_sales_handler():
    """查询所有销售"""
    req = GetAllSalesSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)

    sales = get_all_sales_service(req)

    return success_json(transform_pagination_data(sales))

@jwt_required()
def update_sales_handler():
    """更新销售"""
    req = UpdateSalesSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    sales = update_sales_service(req)
    return success_json(sales.to_dict())