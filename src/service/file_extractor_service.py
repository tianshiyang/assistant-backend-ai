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

from utils import count_tokens


def load_file_from_url(url) -> tuple[List[Document], int, int]:
    """从URL中加载文件
        返回值： langchain的Document列表，token数量，文档字数
    """
    request = requests.get(url)
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, os.path.basename(url))
        with open(path, "wb") as f:
            f.write(request.content)
        return get_document(path), count_tokens(request.content), len(request.content)

def get_document(file_path) -> List[Document]:
   """获取文档"""
   file_extension = Path(file_path).suffix.lower()
   if file_extension in [".docx", '.doc']:
       loader = UnstructuredWordDocumentLoader(file_path)
   else:
       loader = UnstructuredLoader(file_path)
   documents = loader.load()
   return get_documents_chunks(documents)

def get_documents_chunks(documents: List[Document]) -> List[Document]:
    """获取分块后的文档"""
    text_spliter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks = text_spliter.split_documents(documents)
    return chunks

if __name__ == "__main__":
    document_chunks = load_file_from_url("https://assistant-ai-1309470436.cos.ap-beijing.myqcloud.com/羞羞的铁拳.docx")
    print(document_chunks[0])
    # for document in document_chunks:
    #     print(document.page_content)