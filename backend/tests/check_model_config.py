"""
检查模型配置
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models import ModelConfig


async def check_model_config():
    """检查模型配置"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ModelConfig).where(ModelConfig.model_id == "zhipu_glm4")
        )
        model = result.scalar_one_or_none()
        
        if model:
            print(f"模型ID: {model.model_id}")
            print(f"模型名称: {model.model_name}")
            print(f"类型: {type(model.model_name)}")
            print(f"提供商: {model.provider}")
        else:
            print("[ERROR] 未找到模型配置")


if __name__ == "__main__":
    asyncio.run(check_model_config())
