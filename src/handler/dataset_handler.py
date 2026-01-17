#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/17 22:42
@Author  : tianshiyang
@File    : dataset_handler.py
"""
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from pkg.response import validate_error_json, success_message
from schema.dataset_schema import CreateDatasetSchema, GetDataSetDetailSchema, UpdateDatasetSchema, DeleteDatasetSchema
from service.dataset_service import create_dataset_service, get_dataset_detail_service, update_dataset_service, \
    delete_dataset_service


@jwt_required()
def create_dataset_handler():
    """创建知识库"""
    req = CreateDatasetSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    user_id = get_jwt_identity()
    create_dataset_service(req, user_id)
    return success_message("创建知识库成功！")

@jwt_required()
def update_dataset_handler():
    """更新知识库"""
    req = UpdateDatasetSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    user_id = get_jwt_identity()
    result = update_dataset_service(req, user_id)
    return success_message(result.to_dict())

@jwt_required()
def delete_dataset_handler():
    """删除知识库"""
    req = DeleteDatasetSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    user_id = get_jwt_identity()
    dataset = delete_dataset_service(req, user_id)
    return success_message(dataset.to_dict())

@jwt_required()
def get_all_dataset_handler():
    """获取所有知识库"""
    pass

@jwt_required()
def get_dataset_detail_handler():
    """获取知识库详情"""
    req = GetDataSetDetailSchema(formdata=request.args)
    
    if not req.validate():
        return validate_error_json(req.errors)


    user_id = get_jwt_identity()

    dataset = get_dataset_detail_service(req, user_id)

    return success_message(dataset.to_dict())
