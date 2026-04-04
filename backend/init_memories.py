"""
初始化记忆配置

创建默认的记忆配置供预设方案使用
"""

import asyncio

from app.db import init_db, get_db
from app.services.memory_service import MemoryService
from app.schemas.memory_config import MemoryConfigCreate


async def init_default_memories():
    """初始化默认记忆配置"""
    
    # 初始化数据库
    await init_db()
    
    # 获取数据库会话
    async for db in get_db():
        service = MemoryService(db)
        
        # 创建默认记忆配置
        default_memories = [
            {
                "memory_name": "短期记忆（10轮）",
                "memory_type": "buffer_window",
                "memory_params": {"window_size": 10}
            },
            {
                "memory_name": "短期记忆（20轮）",
                "memory_type": "buffer_window",
                "memory_params": {"window_size": 20}
            },
            {
                "memory_name": "Token限制记忆（2K）",
                "memory_type": "token_buffer",
                "memory_params": {"max_tokens": 2000}
            },
            {
                "memory_name": "Token限制记忆（4K）",
                "memory_type": "token_buffer",
                "memory_params": {"max_tokens": 4000}
            },
            {
                "memory_name": "对话摘要",
                "memory_type": "summary",
                "memory_params": {}
            }
        ]
        
        for memory_data in default_memories:
            try:
                # 检查是否已存在
                existing = await service.list_memory_configs(skip=0, limit=100)
                exists = any(m.memory_name == memory_data["memory_name"] for m in existing)
                
                if exists:
                    print(f"[INIT] Memory config '{memory_data['memory_name']}' already exists, skipping...")
                    continue
                
                # 创建记忆配置
                config = await service.create_memory_config(
                    MemoryConfigCreate(**memory_data)
                )
                print(f"[INIT] Created memory config: {config.memory_name} ({config.memory_id})")
                
            except Exception as e:
                print(f"[INIT] Failed to create memory config '{memory_data['memory_name']}': {e}")
        
        break  # 退出数据库会话
    
    print("\n[INIT] Memory configs initialization completed!")


if __name__ == "__main__":
    asyncio.run(init_default_memories())
