#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/28 15:23
@Author  : tianshiyang
@File    : message_service.py
"""
from model.message import Message


def create_message_service(
        conversation_id: str,
        user_id: str,
        question: str,
        messages: str,
        answer: str,
        input_tokens: int,
        output_tokens: int,
        total_tokens: int,
) -> Message:
    """创建一条消息"""
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        question=question,
        messages=messages,
        answer=answer,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
    ).create()
    return message