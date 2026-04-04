#!/usr/bin/env python3
"""
HAXAtom 后端快速启动脚本

一键启动后端服务，自动检查环境并初始化
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.absolute()

def print_header():
    """打印启动标题"""
    print("\n" + "=" * 60)
    print("  HAXAtom 后端服务启动器")
    print("=" * 60 + "\n")

def check_venv():
    """检查虚拟环境"""
    venv_path = PROJECT_ROOT / ".venv"
    if not venv_path.exists():
        print("[X] 虚拟环境不存在")
        print("    请先创建虚拟环境: python -m venv .venv")
        return False
    
    # 检查是否在虚拟环境中
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("[OK] 已在虚拟环境中")
        return True
    else:
        print("[!] 未在虚拟环境中，尝试激活...")
        return False

def check_database():
    """检查数据库文件"""
    db_path = PROJECT_ROOT / "data" / "haxatom.db"
    if db_path.exists():
        print(f"[OK] 数据库存在: {db_path}")
        return True
    else:
        print(f"[!] 数据库不存在: {db_path}")
        print("    将自动初始化数据库")
        return False

def init_database():
    """初始化数据库"""
    print("\n[*] 初始化数据库...")
    
    try:
        # 导入并运行初始化
        sys.path.insert(0, str(PROJECT_ROOT))
        
        async def do_init():
            # 先创建表
            from app.db.session import init_db
            await init_db()
            # 再插入数据
            from app.db.init_data import init_default_data
            await init_default_data()
        
        asyncio.run(do_init())
        print("[OK] 数据库初始化完成")
        return True
        
    except Exception as e:
        print(f"[X] 数据库初始化失败: {e}")
        return False

def start_server():
    """启动服务器"""
    print("\n[*] 启动后端服务...")
    print("    访问地址: http://127.0.0.1:8000")
    print("    API文档:  http://127.0.0.1:8000/docs")
    print("    按 Ctrl+C 停止服务\n")
    print("-" * 60 + "\n")
    
    # 使用 uvicorn 启动
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload",  # 开发模式自动重载
        "--log-level", "info"
    ]
    
    try:
        subprocess.run(cmd, cwd=PROJECT_ROOT)
    except KeyboardInterrupt:
        print("\n\n[*] 服务已停止")
        sys.exit(0)

def main():
    """主函数"""
    print_header()
    
    # 检查虚拟环境
    in_venv = check_venv()
    if not in_venv:
        # 尝试使用虚拟环境的 Python
        venv_python = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
        if venv_python.exists():
            print(f"    使用虚拟环境 Python: {venv_python}")
            # 重新启动脚本使用虚拟环境
            os.execl(str(venv_python), str(venv_python), __file__)
        else:
            print("[X] 无法找到虚拟环境 Python")
            sys.exit(1)
    
    # 检查数据库
    db_exists = check_database()
    if not db_exists:
        # 初始化数据库
        if not init_database():
            print("[X] 启动失败: 数据库初始化错误")
            sys.exit(1)
    
    # 启动服务
    start_server()

if __name__ == "__main__":
    main()
