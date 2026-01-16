#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/13
@Author  : tianshiyang
@File    : base_model.py
数据库模型基类
"""
import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from config.db_config import db


class BaseModel(db.Model):
    """
    数据库模型基类
    提供通用的字段和方法
    """
    __abstract__ = True  # 声明这是一个抽象基类，不会创建表

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=db.text("now()"),
        comment="创建时间"
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=db.text("now()"),
        comment="更新时间",
    )
    
    def to_dict(self):
        """
        将模型转换为字典
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result
    
    def create(self):
        """保存到数据库"""
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """从数据库删除"""
        try:
            db.session.delete(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'
