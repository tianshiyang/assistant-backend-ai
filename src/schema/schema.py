
#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/27 15:51
@Author  : tianshiyang
@File    : schema.py
"""
from wtforms import Field


class ListField(Field):
    """自定义 list 字段，用于存储列表型数据（如 JSON body 中的数组）。"""

    def __init__(self, label=None, validators=None, default=None, **kwargs):
        # 初始化父类，并设置默认值为空列表
        if default is None:
            default = []
        super().__init__(label, validators, default=default, **kwargs)
        # 确保 data 被初始化为列表（即使父类没有设置）
        if not hasattr(self, 'data') or self.data is None:
            self.data = []

    def process_formdata(self, valuelist):
        """处理表单数据：valuelist 是列表，可能包含一个 JSON 数组字符串或直接是列表。"""
        # 确保 self.data 存在
        if not hasattr(self, 'data'):
            self.data = []
        
        if valuelist and len(valuelist) > 0:
            value = valuelist[0]
            # 如果传入的是 JSON 字符串，尝试解析
            if isinstance(value, str):
                import json
                try:
                    self.data = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    self.data = []
            elif isinstance(value, list):
                self.data = value
            else:
                self.data = []
        else:
            self.data = []

    def _value(self):
        """返回字段值（用于表单渲染）。"""
        if not hasattr(self, 'data') or self.data is None:
            return []
        return self.data


class DictField(Field):
    """自定义字典字段，用于存储字典型数据（如 JSON body 中的对象）。"""

    def __init__(self, label=None, validators=None, default=None, **kwargs):
        # 初始化父类，并设置默认值为空字典
        if default is None:
            default = {}
        super().__init__(label, validators, default=default, **kwargs)
        # 确保 data 被初始化为字典（即使父类没有设置）
        if not hasattr(self, 'data') or self.data is None:
            self.data = {}

    def process_formdata(self, valuelist):
        """处理表单数据：valuelist 是列表，可能包含一个 JSON 对象字符串或直接是字典。"""
        # 确保 self.data 存在
        if not hasattr(self, 'data'):
            self.data = {}
        
        if valuelist and len(valuelist) > 0:
            value = valuelist[0]
            # 如果传入的是 JSON 字符串，尝试解析
            if isinstance(value, str):
                import json
                try:
                    self.data = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    self.data = {}
            elif isinstance(value, dict):
                self.data = value
            else:
                self.data = {}
        else:
            self.data = {}

    def _value(self):
        """返回字段值（用于表单渲染）。"""
        if not hasattr(self, 'data') or self.data is None:
            return {}
        return self.data
