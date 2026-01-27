#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/26 18:26
@Author  : tianshiyang
@File    : ai.py
"""
from enum import Enum

SUMMARIZATION_MIDDLEWARE_PROMPT = """
你是一个高级多智能体系统的记忆摘要器。请根据以下完整的对话历史，生成一段简洁、连贯、信息完整的第三人称摘要，用于后续对话的上下文压缩。

摘要需包含：
1. 用户的核心目标或问题；
2. 已调用的工具/技能（如：知识库检索、网络搜索、SQL 查询、深度推理等）及其关键结果；
3. 已达成的中间结论或决策；
4. 尚未解决的子问题或待办事项（如有）。

要求：
- 使用客观、中立的语气；
- 避免直接引用对话原文，应进行归纳；
- 不添加原始对话中未出现的信息；
- 长度控制在 150 字以内。

对话历史：
{chat_history}
"""


class Skills(str, Enum):
    """AI技能"""
    DATASET_RETRIEVER = ("dataset_retriever", "知识库检索")
    TEXT_TO_SQL = ("text_to_sql", "文本转SQL")

    def __new__(cls, value: str, label: str):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj