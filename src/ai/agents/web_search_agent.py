#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/3 23:46
@Author  : tianshiyang
@File    : web_search_agent.py
"""
import asyncio
import json
import os
from typing import List, TypedDict, Callable

import dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from ai import chat_qianwen_llm

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

async def create_web_search_agent(func: Callable[[str], None]):
    class ResponseFormat(TypedDict):
        content: str # 检索出来的内容
        url: str # 检索出来的网站url
        title: str # 检索出来的网站名称

    """创建web搜索Agent"""
    func("正在获取工具")
    tools = await get_mcp_tools()
    func(f"获取工具完成: {tools}")

    # 创建 agent，将 MCP 工具传入
    agent = create_agent(
        model=chat_qianwen_llm,
        tools=tools,
        response_format=ResponseFormat
    )

    # 使用 ainvoke() 异步调用 agent（因为 MCP 工具是异步的）
    func("\nAgent 开始处理，流式输出:")

    result = await agent.ainvoke({
        "messages": [HumanMessage(content="今日上证50指数在多少点")]
    })

    print(result)

    # messages = result["messages"]
    # print(messages)
    # print("=" * 50)
    # for message in messages:
    #     if isinstance(message, ToolMessage):
    #         for page_item in message.content:
    #             if page_item["type"] == "text" and page_item['text'] is not None:
    #                 pages = json.loads(page_item["text"])['pages']
    #                 for page in pages:
    #                     print(f"检索出来的片段{page['snippet']}, 检索出来的网站{page['title']}，网站路径{page['url']}, 网站logo:")
    #     # print("#" * 20)
    #     # print(message)


if __name__ == "__main__":
    def callback(value):
        print(value)
    asyncio.run(create_web_search_agent(callback))