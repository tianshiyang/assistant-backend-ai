#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/25 14:29
@Author  : tianshiyang
@File    : qianwen.py
"""
import os

import dotenv
from langchain_qwq import ChatQwen

dotenv.load_dotenv()

# 阿里千问模型
chat_qianwen_llm = ChatQwen(
    model="qwen3-max",
    temperature=0.7,
    base_url=os.getenv('QWEN_BASE_URL'),
    api_key=os.getenv('QWEN_API_KEY'),
)

if __name__ == "__main__":
    chat = chat_qianwen_llm.invoke("你是那个模型")
    print(chat)