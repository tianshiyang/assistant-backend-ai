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
from schema.sales_schema import GetSalesByIdSchema
from service.sales_service import get_sales_by_id_service


@jwt_required()
def get_sales_by_id_handler():
    req = GetSalesByIdSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)

    sales = get_sales_by_id_service(req)
    return success_json(sales.to_dict())
