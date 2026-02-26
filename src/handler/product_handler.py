#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/17 20:56
@Author  : tianshiyang
@File    : product_handler.py
"""
from flask import request

from pkg.response import validate_error_json, success_json, success_message
from schema.product_schema import GetProductCategoryListSchema, GetProductListSchema, GetProductCategoryListAllSchema, \
    GetProductDetailSchema, ProductUpdateSchema, ProductCreateSchema, DeleteProductSchema, GetProductListAllSchema
from service.product_service import get_product_category_list_service, get_product_list_service, \
    get_product_category_list_all_service, get_product_detail_service, update_product_service, create_product_service, \
    delete_product_service, get_product_list_all_service
from utils import transform_pagination_data


def get_product_category_list_handler():
    """获取商品分类列表"""
    req = GetProductCategoryListSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    paginate = get_product_category_list_service(req)
    return success_json(transform_pagination_data(paginate))

def get_product_category_list_all_handler():
    """获取商品分类列表，不分页"""
    req = GetProductCategoryListAllSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    result = get_product_category_list_all_service(req)
    return success_json([item.to_dict() for item in result])

def get_product_list_handler():
    """获取商品列表"""
    req = GetProductListSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    paginate = get_product_list_service(req)
    return success_json(transform_pagination_data(paginate))

def get_product_list_all_handler():
    """获取所有商品不分页"""
    req = GetProductListAllSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    products = get_product_list_all_service(req)
    return success_json([item.to_dict() for item in products])

def get_product_detail_handler():
    """获取商品详情"""
    req = GetProductDetailSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    result = get_product_detail_service(req.id.data)
    return success_json(result.to_dict())

def update_product_handler():
    """更新商品"""
    req = ProductUpdateSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    result = update_product_service(req)
    return success_json(result.to_dict())

def create_product_handler():
    """新增商品"""
    req = ProductCreateSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    result = create_product_service(req)
    return success_json(result.to_dict())

def delete_product_handler():
    """删除商品"""
    req = DeleteProductSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    delete_product_service(req)
    return success_message("删除成功")
