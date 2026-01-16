#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/16 17:53
@Author  : tianshiyang
@File    : time_format.py
"""
from datetime import datetime


def format_time(time: str) -> str:
    """转化时间为 2026-01-01 00:00:00 格式"""
    dt = datetime.fromisoformat(time)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    print(format_time("2026-01-16 14:45:07.977497+08"))