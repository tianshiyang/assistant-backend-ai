#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/19 22:03
@Author  : tianshiyang
@File    : document_handler.py
"""
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from pkg.response import success_message, validate_error_json, success_json
from schema.document_schema import DocumentUploadToMilvusSchema, DocumentGetAllListSchema, DocumentDeleteSchema
from service.document_service import document_upload_service, document_get_all_list_service, document_delete_service
from utils import transform_pagination_data


@jwt_required()
def document_upload_handler():
    """上传文件到milvus"""
    req = DocumentUploadToMilvusSchema()

    if not req.validate():
        return validate_error_json(req.errors)

    user_id = get_jwt_identity()

    document_upload_service(req, user_id)
    return success_message("插入成功")

@jwt_required()
def document_get_all_list_handler():
    """获取所有文件"""
    req = DocumentGetAllListSchema(request.args)
    if not req.validate():
        return validate_error_json(req.errors)
    user_id = get_jwt_identity()
    pagination = document_get_all_list_service(req, user_id)
    return success_json(transform_pagination_data(pagination))

@jwt_required()
def document_delete_handler():
    """删除文档，同时异步删除Milvus中的数据"""
    req = DocumentDeleteSchema()
    if not req.validate():
        return validate_error_json(req.errors)
    user_id = get_jwt_identity()
    document = document_delete_service(req, user_id)
    return success_json(document.to_dict())