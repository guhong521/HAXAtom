"""
修复模型配置

将 model_name 从列表改为字符串
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models import ModelConfig


async def fix_model_config():
    """修复模型配置"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ModelConfig).where(ModelConfig.model_id == "zhipu_glm4")
        )
        model = result.scalar_one_or_none()
        
        if model:
            # 检查 model_name 是否为列表
            if isinstance(model.model_name, list):
                model.model_name = model.model_name[0]  # 取第一个
                await session.commit()
                print(f"[OK] 已修复模型配置: {model.model_name}")
            else:
                print(f"[INFO] 模型配置正常: {model.model_name}")
        else:
            print("[ERROR] 未找到模型配置")


if __name__ == "__main__":
    asyncio.run(fix_model_config())
