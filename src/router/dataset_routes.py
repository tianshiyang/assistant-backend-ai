#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/17 22:33
@Author  : tianshiyang
@File    : dataset_routes.py
"""
from flask import Blueprint

from handler.dataset_handler import create_dataset_handler, update_dataset_handler, delete_dataset_handler, \
    get_all_dataset_handler, get_dataset_detail

"""知识库创建相关路由"""
dataset_blueprint = Blueprint("dataset", __name__, url_prefix="")

# 创建知识库
dataset_blueprint.add_url_rule("/api/dataset/create", methods=["POST"], view_func=create_dataset_handler)
# 更新知识库
dataset_blueprint.add_url_rule("/api/dataset/update", methods=["POST"], view_func=update_dataset_handler)
# 删除知识库
dataset_blueprint.add_url_rule("/api/dataset/delete", methods=["POST"], view_func=delete_dataset_handler)
# 获取所有知识库
dataset_blueprint.add_url_rule("api/dataset/getAllDataset", methods=["GET"], view_func=get_all_dataset_handler)
# 通过id获取知识库详情
dataset_blueprint.add_url_rule("/api/dataset/datasetDetail", methods=["GET"], view_func=get_dataset_detail)