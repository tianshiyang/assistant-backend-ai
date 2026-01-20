#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/19 22:03
@Author  : tianshiyang
@File    : document_handler.py
"""
from flask_jwt_extended import jwt_required, get_jwt_identity

from pkg.response import success_message, validate_error_json
from schema.document_schema import DocumentUploadToMilvusSchema
from service.document_service import document_upload_service


@jwt_required()
def document_upload_handler():
    """上传文件到milvus"""
    req = DocumentUploadToMilvusSchema()

    if not req.validate():
        return validate_error_json(req.errors)

    user_id = get_jwt_identity()

    document_upload_service(req, user_id)
    return success_message("插入成功")