#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
密码哈希生成工具
用于生成用户密码的哈希值，存储在数据库中

使用方法:
    python scripts/generate_password_hash.py <password>
    
示例:
    python scripts/generate_password_hash.py mypassword123
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pkg.security import generate_password_hash


def main():
    if len(sys.argv) < 2:
        print("用法: python scripts/generate_password_hash.py <password>")
        print("示例: python scripts/generate_password_hash.py mypassword123")
        sys.exit(1)
    
    password = sys.argv[1]
    hashed = generate_password_hash(password)
    
    print(f"原始密码: {password}")
    print(f"哈希值: {hashed}")
    print("\n请将哈希值存储到数据库中，不要存储原始密码！")


if __name__ == '__main__':
    main()
