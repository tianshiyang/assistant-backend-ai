#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/19 22:19
@Author  : tianshiyang
@File    : embeddings.py
"""
import os

import dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from transformers import AutoTokenizer

dotenv.load_dotenv()

embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
)

tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    trust_remote_code=True
)

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

if __name__ == "__main__":
    test_text = "这是一个用于向量化的测试文本"
    tokens = count_tokens(test_text)

    print(tokens, tokenizer.encode(test_text))