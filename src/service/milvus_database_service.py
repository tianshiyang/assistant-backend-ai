#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/19 22:08
@Author  : tianshiyang
@File    : milvus_database_service.py
"""
import os
from uuid import uuid4

from langchain_core.documents import Document
from langchain_milvus import Milvus, BM25BuiltInFunction

from utils import embeddings

def add_documents():
    document_1 = Document(
        page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.",
        metadata={"source": "tweet"},
    )

    document_2 = Document(
        page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
        metadata={"source": "news"},
    )

    document_3 = Document(
        page_content="Building an exciting new project with LangChain - come check it out!",
        metadata={"source": "tweet"},
    )

    document_4 = Document(
        page_content="Robbers broke into the city bank and stole $1 million in cash.",
        metadata={"source": "news"},
    )

    document_5 = Document(
        page_content="Wow! That was an amazing movie. I can't wait to see it again.",
        metadata={"source": "tweet"},
    )

    document_6 = Document(
        page_content="Is the new iPhone worth the price? Read this review to find out.",
        metadata={"source": "website"},
    )

    document_7 = Document(
        page_content="The top 10 soccer players in the world right now.",
        metadata={"source": "website"},
    )

    document_8 = Document(
        page_content="LangGraph is the best framework for building stateful, agentic applications!",
        metadata={"source": "tweet"},
    )

    document_9 = Document(
        page_content="The stock market is down 500 points today due to fears of a recession.",
        metadata={"source": "news"},
    )

    document_10 = Document(
        page_content="I have a bad feeling I am going to get deleted :(",
        metadata={"source": "tweet"},
    )

    documents = [
        document_1,
        document_2,
        document_3,
        document_4,
        document_5,
        document_6,
        document_7,
        document_8,
        document_9,
        document_10,
    ]
    uuids = [str(uuid4()) for _ in range(len(documents))]

    get_milvus_client().add_documents(documents=documents, ids=uuids)


def get_milvus_client():
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
        collection_name="test_db_collection",
        connection_args={
            "uri": os.getenv("MILVUS_URI"),
            "db_name": os.getenv("MILVUS_DB_NAME", "default"),
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