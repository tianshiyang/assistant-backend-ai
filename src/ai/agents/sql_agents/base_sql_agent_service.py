#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/28 11:15
@Author  : tianshiyang
@File    : base_sql_agent_service.py
"""
import os

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

from ai import chat_qianwen_llm
from ai.service import BaseAgentService
from utils import build_mysql_uri


class BaseSQLAgentService(BaseAgentService):
    """基础SQLAgent"""
    def __init__(self, conversation_id: str) -> None:
        self.conversation_id = conversation_id
        self.db_uri = os.getenv("POSTGRES_SHOT_MEMORY_URI")
        self.config = self.get_config(conversation_id=self.conversation_id)
        self.db = self.get_database_db()
        self.tools = self.get_sql_database_tools()
        self.sql_description = self.get_tables_description()

    def get_sql_database_tools(self):
        """加载数据库"""
        toolkit = SQLDatabaseToolkit(db=self.db, llm=chat_qianwen_llm)
        tools = toolkit.get_tools()
        return tools

    def get_tables_description(self) -> str:
        """获取mysql表格的描述信息"""
        db_schema_tool = None
        db_list_tool = None
        for tool in self.tools:
            if tool.name == "sql_db_schema":
                db_schema_tool = tool
        if not db_schema_tool and not db_list_tool:
            return "未找到任何表内容"
        return db_schema_tool.invoke(",".join(self.db.get_usable_table_names()))

    @staticmethod
    def get_database_db():
        """获取数据库对象"""
        return SQLDatabase.from_uri(build_mysql_uri())