#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/19 22:00
@Author  : tianshiyang
@File    : document_router.py
"""
from flask import Blueprint

from handler.document_handler import document_upload_handler

document_router = Blueprint('document_router', __name__, url_prefix="")

document_router.add_url_rule("/api/document/upload", methods=["POST"], view_func=document_upload_handler)