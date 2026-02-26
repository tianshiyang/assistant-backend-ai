#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/25 22:17
@Author  : tianshiyang
@File    : order_schema.py
"""
from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired

from schema.base_schema import PaginationSchema


class GetOrderListSchema(PaginationSchema):
    """获取商品列表"""
    order_no = StringField(validators=[])

class GetOrderDetailSchema(FlaskForm):
    """获取商品列表"""
    order_id = IntegerField(validators=[DataRequired("订单id必传")])

class CreateOrderSchema(FlaskForm):
    sales_id = IntegerField(validators=[DataRequired("销售id必传")])
    customer_id = IntegerField(validators=[DataRequired("客户id必传")])
    product_id = IntegerField(validators=[DataRequired("商品id必传")])
    quantity = IntegerField(validators=[DataRequired("购买数量必传")])

class PayOrderSchema(FlaskForm):
    order_id = IntegerField(validators=[DataRequired("订单id必传")])
    pay_amount = IntegerField(validators=[DataRequired("支付金额必传")])

class CancelPayOrderSchema(FlaskForm):
    order_id = IntegerField(validators=[DataRequired("订单id必传")])

class DeleteOrderSchema(FlaskForm):
    order_id = IntegerField(validators=[DataRequired("订单id必传")])
