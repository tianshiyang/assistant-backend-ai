#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/19 22:08
@Author  : tianshiyang
@File    : milvus_database_service.py
"""
import os
import uuid
from typing import List

from langchain_core.documents import Document
from langchain_milvus import Milvus, BM25BuiltInFunction

from utils import embeddings

def add_documents(documents: List[Document], user_id: str, document_id: str, dataset_id: str, source: str):
    """添加文档"""
    # 为每个文档添加元数据
    for document in documents:
        document.metadata['user_id'] = user_id
        document.metadata['dataset_id'] = dataset_id
        document.metadata['source'] = source
        document.metadata['document_id'] = document_id
    
    # 生成唯一 ID
    ids = [str(uuid.uuid4()) for _ in documents]
    
    # 添加到 Milvus
    get_milvus_client().add_documents(
        documents=documents,
        ids=ids
    )

def delete_documents(user_id: str, document_id = None, dataset_id: str = None):
    """删除文档"""
    vector_store = get_milvus_client()
    expr = ""
    if dataset_id:
        expr = f"user_id == '{user_id}' AND dataset_id == '{dataset_id}'"
    if document_id:
        expr = f"user_id == '{user_id}' AND document_id == '{document_id}'"
    vector_store.delete(
        expr=expr
    )

def get_milvus_client(collection_name: str = "assistant_ai_dataset_documents"):
    """获取 Milvus 数据库客户端"""
    dense_index_param = {
        "metric_type": "COSINE",
        "index_type": "HNSW",
    }
    sparse_index_param = {
        "metric_type": "BM25",
        "index_type": "AUTOINDEX",
    }
    return Milvus(
        index_params=[dense_index_param, sparse_index_param],
        collection_name=collection_name,
        connection_args={
            "uri": os.getenv("MILVUS_URI"),
            "db_name": os.getenv("MILVUS_DB_NAME"),
            "token": os.getenv("MILVUS_TOKEN"),
        },
        embedding_function=embeddings,
        vector_field=["dense", "sparse"],
        primary_field="id",
        builtin_function=BM25BuiltInFunction(
            function_name="bm25",
        ),
        enable_dynamic_field=True,
    )

def get_retriever(
        k: int = 10,
        expr: str = "",
        dense_weight: float = 0.7,
        sparse_weight: float = 0.3,
        ef: int = None,
):
    """
    获取检索器
    
    Args:
        k: 返回的文档数量（建议设置为实际需要的2-3倍，然后取前k个）
        expr: Milvus 过滤表达式，如 'user_id == "xxx" and dataset_id == "yyy"'
        dense_weight: Dense向量（语义相似度）的权重，范围 0-1
        sparse_weight: Sparse向量（BM25关键词匹配）的权重，范围 0-1
        ef: HNSW 搜索参数，值越大搜索越精确但越慢（默认使用索引的ef值）
    
    Returns:
        Retriever: LangChain 检索器实例
    
    Note:
        - 权重建议：对于语义理解类查询，dense_weight 可以更高（0.7-0.8）
        - 对于关键词匹配类查询，sparse_weight 可以更高（0.5-0.6）
        - 权重会自动归一化，总和不需要等于1
    """
    vectorstore = get_milvus_client()

    # 归一化权重
    total_weight = dense_weight + sparse_weight
    if total_weight > 0:
        dense_weight = dense_weight / total_weight
        sparse_weight = sparse_weight / total_weight
    
    search_kwargs = {
        "k": k,
    }
    
    if expr:
        search_kwargs["expr"] = expr
    
    if ef is not None:
        search_kwargs["ef"] = ef
    
    return vectorstore.as_retriever(
        search_type="similarity",
        ranker_type="weighted",
        ranker_params={"weights": [dense_weight, sparse_weight]},
        search_kwargs=search_kwargs
    )


def get_retriever_with_scores(
        query: str,
        k: int = 20,
        expr: str = "",
        dense_weight: float = 0.7,
        sparse_weight: float = 0.3,
        final_k: int = None,
        min_score: float = None,
):
    """
    获取检索结果并返回分数（用于调试和优化）
    
    Args:
        query: 查询文本
        k: 初始检索数量（建议设置为最终需要的2-3倍）
        expr: 过滤表达式
        dense_weight: Dense向量权重
        sparse_weight: Sparse向量权重
        final_k: 最终返回的数量（如果为None，返回所有结果）
        min_score: 最小分数阈值（过滤低分结果）
    
    Returns:
        List[Tuple[Document, float]]: (文档, 分数) 的列表，分数越高越相关
    """
    vectorstore = get_milvus_client()
    
    # 归一化权重
    total_weight = dense_weight + sparse_weight
    if total_weight > 0:
        dense_weight = dense_weight / total_weight
        sparse_weight = sparse_weight / total_weight
    
    search_kwargs = {"k": k}
    if expr:
        search_kwargs["expr"] = expr
    
    # 使用带分数的搜索
    docs_with_scores = vectorstore.similarity_search_with_score(
        query,
        ranker_type="weighted",
        ranker_params={"weights": [dense_weight, sparse_weight]},
        **search_kwargs
    )
    
    # 过滤低分结果
    if min_score is not None:
        docs_with_scores = [(doc, score) for doc, score in docs_with_scores if score >= min_score]
    
    # 取前 final_k 个
    if final_k is not None:
        docs_with_scores = docs_with_scores[:final_k]
    
    return docs_with_scores

if __name__ == "__main__":
    delete_documents(user_id="749d17ca-4227-4127-b94a-12ec8ff451dd", dataset_id="ce949e61-4e52-4aeb-a97c-8aa77dea0f0f")
    # cur_user_id = "749d17ca-4227-4127-b94a-12ec8ff451dd"
    # cur_dataset_id = "2e949e61-4e52-4aeb-a97c-8aa77dea0f0f"
    # query = "电影《羞羞的铁拳》什么时候上映的"
    #
    # # 方式1: 使用带分数的检索（推荐，可以查看相关性分数）
    # results_with_scores = get_retriever_with_scores(
    #     query=query,
    #     k=20,  # 获取更多候选结果
    #     expr=f'user_id == "{cur_user_id}"',
    #     dense_weight=0.7,  # 语义相似度权重（对于这类问题可以调高）
    #     sparse_weight=0.3,  # 关键词匹配权重
    #     final_k=5,  # 最终返回前5个最相关的结果
    #     min_score=0.3,  # 过滤掉分数低于0.3的结果
    # )
    #
    # print(f"找到 {len(results_with_scores)} 个相关结果:\n")
    # for i, (doc, score) in enumerate(results_with_scores, 1):
    #     print(f"[{i}] 分数: {score:.4f}")
    #     print(f"内容: {doc.page_content[:100]}...")
    #     print(f"元数据: {doc.metadata}\n")
    
    # # 方式2: 使用普通检索器
    # print("\n=== 方式2: 普通检索器 ===")
    # my_retriever = get_retriever(
    #     k=5,  # 直接返回5个结果
    #     expr=f'user_id == "{cur_user_id}"',
    #     dense_weight=0.7,  # 可以尝试调整权重
    #     sparse_weight=0.3,
    # )
    # results = my_retriever.invoke(query)
    #
    # for i, result in enumerate(results, 1):
    #     print(f"[{i}] {result.page_content[:100]}...")