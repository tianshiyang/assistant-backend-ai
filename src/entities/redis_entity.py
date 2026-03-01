#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/27 23:19
@Author  : tianshiyang
@File    : redis_entity.py
"""
# 存储聊天接口中，调用AI返回结果的chunks
REDIS_CHAT_GENERATED_KEY = "redis:stream:chat:generated:{conversation_id}"

# 终止会话继续相应
REDIS_CHAT_STOP_KEY = "redis:stream:chat:stop:{conversation_id}"

# 存储Text2Sql的Agent聊天接口，返回结果的chunks
REDIS_TEXT_TO_SQL_KEY = "redis:stream:chat:text2sql:{conversation_id}"

# 停止Text2Sql生成
REDIS_TEXT_STOP_TEXT_TO_SQL = "redis:stream:chat:text2sql:stop:{conversation_id}"
