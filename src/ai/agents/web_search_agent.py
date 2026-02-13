#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/3 23:46
@Author  : tianshiyang
@File    : web_search_agent.py
"""
import json
import os
from typing import List

import dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool, tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import ToolRuntime

from ai import chat_qianwen_llm
from ai.prompts.prompts import WEB_SEARCH_AGENT_PROMPTS
from entities.chat_response_entity import SearchToolProcessDataSchema, AgentContextSchema, ChatResponseType
from utils import get_module_logger

logger = get_module_logger(__name__)

dotenv.load_dotenv()

mcp_clients = {
    "WebSearch": {
        "transport": "sse",
        "url": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/sse",
        "headers": {
            "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
        }
    }
}


async def get_mcp_tools() -> List[BaseTool]:
    """使用 MCP 工具调用外部服务"""
    client = MultiServerMCPClient(mcp_clients)
    tools = await client.get_tools()
    return tools


@tool
async def web_search_agent_tool(query: str, runtime: ToolRuntime[AgentContextSchema]) -> str:
    """
    Web 搜索工具：使用 MCP 工具在互联网上检索信息并生成回答。

    Args:
        query: 要搜索的问题或关键词

    Returns:
        搜索结果的 JSON 字符串
    """
    try:
        callable_func = runtime.context.get("function_callable")
        callable_func(ChatResponseType.GET_TOOLS, f"正在获取mcp可使用的工具")
        tools = await get_mcp_tools()
        logger.info(f"获取 MCP 工具完成: {[t.name for t in tools]}")

        # 创建子 agent，将 MCP 工具传入
        agent = create_agent(
            model=chat_qianwen_llm,
            tools=tools,
            response_format=SearchToolProcessDataSchema,
            system_prompt=WEB_SEARCH_AGENT_PROMPTS
        )

        result = await agent.ainvoke({
            "messages": [HumanMessage(content=query)]
        })

        structured = result.get("structured_response")
        if structured is None:
            logger.warning("Agent did not return structured_response, using empty result")
            fallback = SearchToolProcessDataSchema(
                tool_process_type="search",
                tool_process_content=[]
            )
            return json.dumps(fallback.model_dump(), ensure_ascii=False)
        return json.dumps(structured.model_dump(), ensure_ascii=False)

    except Exception as e:
        logger.error(f"Web 搜索执行出错: {e}", exc_info=True)
        return f"Web 搜索执行出错: {type(e).__name__}: {e}"
