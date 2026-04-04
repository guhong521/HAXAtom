"""
测试资源校验功能

验证 preset_engine.validate_preset_resources() 是否正确工作
"""

import asyncio
import sys
sys.path.insert(0, 'f:\\2025python\\HAXAtom\\backend')

from app.db.session import AsyncSessionLocal
from app.core import PresetEngine


async def test_valid_preset():
    """测试有效预设方案"""
    print("=" * 60)
    print("测试1: 有效预设方案（应该通过）")
    print("=" * 60)
    
    async with AsyncSessionLocal() as session:
        engine = PresetEngine(session)
        
        try:
            preset = await engine.load_preset("test_preset")
            await engine.validate_preset_resources(preset)
            print("[PASS] 资源校验通过")
            return True
        except ValueError as e:
            print(f"[FAIL] 资源校验失败: {e}")
            return False


async def test_invalid_model():
    """测试无效模型ID"""
    print("\n" + "=" * 60)
    print("测试2: 无效模型ID（应该报错）")
    print("=" * 60)
    
    async with AsyncSessionLocal() as session:
        engine = PresetEngine(session)
        
        # 创建一个模拟的预设对象
        from app.models import Preset
        preset = Preset(
            preset_id="test_invalid",
            preset_name="测试预设",
            selected_model="nonexistent_model",
            selected_prompt=None,
            selected_plugins=[],
            selected_knowledge_bases=[],
            selected_memory=None
        )
        
        try:
            await engine.validate_preset_resources(preset)
            print("[FAIL] 应该报错但没有")
            return False
        except ValueError as e:
            print(f"[PASS] 正确报错: {e}")
            return True


async def test_invalid_plugin():
    """测试无效插件ID"""
    print("\n" + "=" * 60)
    print("测试3: 无效插件ID（应该报错）")
    print("=" * 60)
    
    async with AsyncSessionLocal() as session:
        engine = PresetEngine(session)
        
        from app.models import Preset
        preset = Preset(
            preset_id="test_invalid_plugin",
            preset_name="测试预设",
            selected_model="zhipu_glm4",
            selected_prompt=None,
            selected_plugins=["nonexistent_plugin"],
            selected_knowledge_bases=[],
            selected_memory=None
        )
        
        try:
            await engine.validate_preset_resources(preset)
            print("[FAIL] 应该报错但没有")
            return False
        except ValueError as e:
            print(f"[PASS] 正确报错: {e}")
            return True


async def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("资源校验功能测试")
    print("=" * 60)
    
    results = []
    
    try:
        results.append(await test_valid_preset())
    except Exception as e:
        print(f"[ERROR] 测试1异常: {e}")
        results.append(False)
    
    try:
        results.append(await test_invalid_model())
    except Exception as e:
        print(f"[ERROR] 测试2异常: {e}")
        results.append(False)
    
    try:
        results.append(await test_invalid_plugin())
    except Exception as e:
        print(f"[ERROR] 测试3异常: {e}")
        results.append(False)
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    print(f"通过: {sum(results)}/{len(results)}")
    
    if all(results):
        print("[SUCCESS] 所有测试通过!")
    else:
        print("[WARNING] 部分测试失败")


if __name__ == "__main__":
    asyncio.run(main())
