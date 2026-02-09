#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/20 09:49
@Author  : tianshiyang
@File    : file_extractor_service.py
"""
import os
import tempfile
from pathlib import Path
from typing import List

import requests
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_unstructured import UnstructuredLoader

from utils import count_tokens, get_module_logger

logger = get_module_logger(__name__)

# ─── 分块参数（可通过环境变量调整） ────────────────────────────────
# chunk_size:    每个分块的最大字符数（中文 1 字 = 1 字符）
# chunk_overlap: 相邻分块的重叠字符数，保证上下文连贯
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# ─── 中文分隔符（优先按段落 → 句子 → 逗号 → 字符拆分） ───────────
_CHINESE_SEPARATORS = [
    "\n\n",     # 段落
    "\n",       # 换行
    "。",       # 句号
    "！",       # 感叹号
    "？",       # 问号
    "；",       # 分号
    "……",      # 省略号
    "…",
    ". ",       # 英文句号
    "! ",
    "? ",
    ";",
    ",",
    "，",       # 中文逗号
    " ",
    "",         # 最终按字符拆
]


def load_file_from_url(url) -> tuple[List[Document], int, int]:
    """从 URL 下载文件并解析为 Document 列表。
    返回值：(document_chunks, token_count, character_count)
    """
    response = requests.get(url)
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, os.path.basename(url))
        with open(path, "wb") as f:
            f.write(response.content)
        return get_document(path), count_tokens(response.content), len(response.content)


def get_document(file_path: str) -> List[Document]:
    """根据文件类型加载文档（支持中文）。"""
    ext = Path(file_path).suffix.lower()

    if ext in (".docx", ".doc"):
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        # languages=["chi_sim", "eng"]  让 tesseract OCR 同时识别中文和英文
        loader = UnstructuredLoader(
            file_path,
            languages=["chi_sim", "eng"],
        )

    documents = loader.load()
    logger.info(f"文档加载完成，共 {len(documents)} 段，文件: {Path(file_path).name}")
    return get_documents_chunks(documents)


def get_documents_chunks(documents: List[Document]) -> List[Document]:
    """使用中文友好的分隔符对文档进行分块。"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=_CHINESE_SEPARATORS,
    )
    chunks = splitter.split_documents(documents)
    logger.info(f"分块完成，共 {len(chunks)} 个片段 (chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


if __name__ == "__main__":
    document_chunks = load_file_from_url("https://assistant-ai-1309470436.cos.ap-beijing.myqcloud.com/羞羞的铁拳.docx")
    print(f"共 {len(document_chunks)} 个分块")
    for i, doc in enumerate(document_chunks[:3], 1):
        print(f"\n[{i}] {doc.page_content[:200]}...")
