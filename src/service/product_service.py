#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/17 20:56
@Author  : tianshiyang
@File    : product_service.py
"""
from datetime import datetime
from typing import List

from sqlalchemy.orm import joinedload

from config.db_config import db
from entities.base_entity import Pagination
from model.mysql_model.product import Product
from model.mysql_model import ProductCategory
from pkg.exception import FailException
from schema.product_schema import GetProductCategoryListSchema, GetProductListSchema, GetProductListAllSchema, \
    GetProductDetailSchema, ProductUpdateSchema, ProductCreateSchema, DeleteProductSchema


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

def get_product_category_list_all_service(req: GetProductListAllSchema) -> List[ProductCategory]:
    """获取商品分类列表 -- 不分页"""
    filter_category = []
    if req.name.data:
        filter_category.append(ProductCategory.name.ilike('%' + req.name.data + '%'))
    category_all_list = db.session.query(ProductCategory).filter(*filter_category).order_by(ProductCategory.created_at.desc()).all()
    return category_all_list

def get_product_list_service(req: GetProductListSchema) -> Pagination[Product]:
    """获取商品列表"""
    filter_product = []

    if req.name.data:
        filter_product.append(Product.name.ilike('%' + req.name.data + '%'))

    if req.category_id.data:
        category_id = int(req.category_id.data)
        filter_product.append(Product.category_id == category_id)

    if req.product_no.data:
        filter_product.append(Product.product_no == req.product_no.data)

    paginate = (
        db.session.query(Product)
        .options(joinedload(Product.category))
        .filter(*filter_product)
        .order_by(Product.created_at.desc())
        .paginate(
            page=int(req.page_no.data),
            per_page=int(req.page_size.data),
            error_out=False
        )
    )

    return paginate

def _generate_product_no() -> str:
    """生成商品编号：P + 年月日(YYYYMMDD) + 当日顺序号(3位)，如 P20260225001。
    查询当日最后一个商品编号，在其基础上 +1；当日无商品则从 001 开始。
    """
    date_part = datetime.now().strftime("%Y%m%d")
    prefix = f"P{date_part}"

    last = (
        db.session.query(Product)
        .filter(Product.product_no.like(f"{prefix}%"), Product.deleted == 0)
        .order_by(Product.product_no.desc())
        .first()
    )

    if last is None:
        seq = 1
    else:
        try:
            # 取编号后 3 位为顺序号
            seq = int(last.customer_no[-3:]) + 1
        except (ValueError, IndexError):
            seq = 1
    if seq > 999:
        raise FailException("当日新增商品已达上限，请明日再试")
    return f"{prefix}{str(seq).zfill(3)}"


def get_product_detail_service(product_id: int) -> Product:
    """获取商品详情"""
    result = db.session.query(Product).filter(
        Product.id == product_id
    ).first()
    if not result:
        raise FailException("商品不存在")
    return result

def update_product_service(req: ProductUpdateSchema) -> Product:
    """更新商品信息"""
    product = get_product_detail_service(req.id.data)
    data = {}
    if req.name.data:
        data["name"] = req.name.data
    if req.category_id.data:
        data["category_id"] = req.category_id.data
    if req.standard_price.data:
        data["standard_price"] = req.standard_price.data
    if req.cost_price.data:
        data["cost_price"] = req.cost_price.data
    product.update(**data)
    return product

def create_product_service(req: ProductCreateSchema) -> Product:
    """新增商品"""
    product_no = _generate_product_no()
    result = Product(
        name=req.name.data,
        product_no=product_no,
        category_id=req.category_id.data,
        standard_price=req.standard_price.data,
        cost_price=req.cost_price.data,
    ).create()
    return result

def delete_product_service(req: DeleteProductSchema) -> Product:
    """删除商品"""
    product = get_product_detail_service(req.id.data)
    product.delete()
    return product
