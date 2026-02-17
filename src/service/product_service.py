#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/17 20:56
@Author  : tianshiyang
@File    : product_service.py
"""
from config.db_config import db
from entities.base_entity import Pagination
from model.mysql_model.product_category import ProductCategory
from schema.product_schema import GetProductCategoryListSchema


def get_product_category_list_service(req: GetProductCategoryListSchema) -> Pagination[ProductCategory]:
    """获取商品分类列表"""
    filters = []
    if req.category_name.data:
        filters.append(ProductCategory.category_name.ilike('%' + req.category_name.data + '%'))
    paginate = db.session.query(ProductCategory).filter(*filters).order_by(ProductCategory.created_at.desc()).paginate(
        page=int(req.page_no.data),
        per_page=int(req.page_size.data),
        error_out=False
    )
    return paginate