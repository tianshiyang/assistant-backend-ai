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
