#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/19 22:00
@Author  : tianshiyang
@File    : document_router.py
"""
from flask import Blueprint

from handler.document_handler import document_upload_handler, document_get_all_list_handler, document_delete_handler

document_blueprint = Blueprint('document_router', __name__, url_prefix="")

# 上传文件并开启解析
document_blueprint.add_url_rule("/api/document/upload", methods=["POST"], view_func=document_upload_handler)
# 获取所有文件
document_blueprint.add_url_rule("/api/document/list", methods=["GET"], view_func=document_get_all_list_handler)
# 删除文档
document_blueprint.add_url_rule("/api/document/delete", methods=["POST"], view_func=document_delete_handler)