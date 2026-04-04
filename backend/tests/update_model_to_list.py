"""
更新模型配置为列表格式
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models import ModelConfig


async def update_model_config():
    """更新模型配置为列表格式"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ModelConfig).where(ModelConfig.model_id == "zhipu_glm4")
        )
        model = result.scalar_one_or_none()
        
        if model:
            # 更新为列表格式
            model.model_name = ["glm-4", "glm-4-flash"]
            await session.commit()
            print(f"[OK] 已更新模型配置为列表: {model.model_name}")
            print(f"类型: {type(model.model_name)}")
        else:
            print("[ERROR] 未找到模型配置")


if __name__ == "__main__":
    asyncio.run(update_model_config())
