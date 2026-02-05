#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/27 23:26
@Author  : tianshiyang
@File    : chat_response_entity.py
"""
import json
from enum import Enum
from typing import Any, TypedDict, NotRequired, Callable
from entities.ai import Skills

class ChatResponseType(str, Enum):
    """
    ping-保持连通
    done-完成
    error-失败
    tool-调用工具
    get_tools-获取可调用的工具
    generate-生成内容
    tool_result-工具返回结果
    tool_process_data-工具执行的过程数据
    generates-生成内容
    create_conversation-生成会话
    """
    PING = "ping"
    DONE = "done"
    ERROR = "error"
    GET_TOOLS = "get_tools"  # 获取可调用的工具
    TOOL_PROCESS = "tool_process_data" # 工具执行的过程数据
    TOOL = "tool"
    TOOL_RESULT = "tool_result"
    SAVE_TOKEN = "save_token"
    GENERATE = "generate"
    CREATE_CONVERSATION = "create_conversation"


# AI返回的响应体
class ChatResponseEntity(TypedDict):
    updated_time: float
    content: Any
    message_id: str
    type: ChatResponseType # AI返回的内容类型
    tool_call: Skills | None
    conversation_id: str

# agent context
class AgentContextSchema(TypedDict):
    dataset_ids: NotRequired[list[str]]
    function_callable: Callable[[ChatResponseType, str], None]

# if __name__ == "__main__":
#     result = ChatResponseEntity(
#         updated_time=123123,
#         content=json.dumps({"name": "张三"}),
#         type = ChatResponseType.PING,
#         tool_call=Skills.DATASET_RETRIEVER
#     )
#
#     print(type(json.dumps(result)), json.dumps(result))
