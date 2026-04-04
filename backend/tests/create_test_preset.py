"""
创建测试预设脚本

用于快速创建测试用的预设方案、提示词配置等
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models import ModelConfig, PromptConfig, Preset


async def create_test_data():
    """创建测试数据"""
    async with AsyncSessionLocal() as session:
        # 1. 检查是否有模型配置
        result = await session.execute(select(ModelConfig))
        models = result.scalars().all()
        
        if not models:
            print("[ERROR] 没有可用的模型配置，请先初始化数据库")
            return
        
        model = models[0]
        print(f"[INFO] 使用模型: {model.model_id}")
        
        # 2. 创建提示词配置
        result = await session.execute(
            select(PromptConfig).where(PromptConfig.prompt_id == "default_assistant")
        )
        prompt = result.scalar_one_or_none()
        
        if not prompt:
            prompt = PromptConfig(
                prompt_id="default_assistant",
                prompt_name="默认助手",
                system_prompt="你是一个 helpful 的 AI 助手，请用中文回答用户的问题。",
                is_active=True
            )
            session.add(prompt)
            await session.commit()
            print("[OK] 提示词配置已创建")
        else:
            print("[INFO] 提示词配置已存在")
        
        # 3. 创建测试预设
        result = await session.execute(
            select(Preset).where(Preset.preset_id == "test_preset")
        )
        preset = result.scalar_one_or_none()
        
        if not preset:
            preset = Preset(
                preset_id="test_preset",
                preset_name="测试预设",
                description="用于测试 LangGraph 工作流的预设方案",
                selected_model=model.model_id,
                selected_prompt="default_assistant",
                selected_memory=None,
                selected_plugins=[],
                selected_knowledge_bases=[],
                is_default=True,
                is_active=True
            )
            session.add(preset)
            await session.commit()
            print("[OK] 测试预设已创建")
        else:
            print("[INFO] 测试预设已存在")
        
        print("\n" + "="*60)
        print("测试数据创建完成！")
        print("="*60)
        print(f"预设ID: test_preset")
        print(f"模型ID: {model.model_id}")
        print(f"提示词ID: default_assistant")
        print("="*60)


if __name__ == "__main__":
    asyncio.run(create_test_data())
