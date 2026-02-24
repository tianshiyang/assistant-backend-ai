#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/17 20:56
@Author  : tianshiyang
@File    : product_service.py
"""
from config.db_config import db
from entities.base_entity import Pagination
from model.mysql_model.product import Product
from model.mysql_model.product_category import ProductCategory
from schema.product_schema import GetProductCategoryListSchema, GetProductListSchema


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

def get_product_list_service(req: GetProductListSchema) -> Pagination[Product]:
    """获取商品列表"""
    filter_product = []

    if req.name.data:
        filter_product.append(Product.name.ilike('%' + req.name.data + '%'))

    paginate = db.session.query(Product).filter(*filter_product).order_by(Product.created_at.desc()).paginate(
        page=int(req.page_no.data),
        per_page=int(req.page_size.data),
        error_out=False
    )

    return paginate