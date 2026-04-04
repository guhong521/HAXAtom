"""
工具调用测试

测试 Agent 自动决策调用插件功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.preset_engine import PresetEngine
from app.db.session import AsyncSessionLocal
from app.plugins import registry
from app.plugins.builtin.calculator_plugin import CalculatorPlugin
from app.plugins.builtin.search_plugin import SearchPlugin
from app.plugins.builtin.time_plugin import TimePlugin


async def init_plugins():
    """初始化内置插件"""
    print("=" * 50)
    print("初始化插件...")
    print("=" * 50)
    
    # 注册内置插件
    registry.register(TimePlugin)
    registry.register(CalculatorPlugin)
    registry.register(SearchPlugin)
    
    # 显示已注册的插件
    plugin_ids = registry.list_plugins()
    print(f"已注册 {len(plugin_ids)} 个插件:")
    for pid in plugin_ids:
        metadata = registry.get_metadata(pid)
        if metadata:
            print(f"  - {metadata.name}: {metadata.description}")
    print()


async def test_direct_plugin_execution():
    """测试直接执行插件"""
    print("=" * 50)
    print("测试1: 直接执行插件")
    print("=" * 50)
    
    # 测试时间插件
    time_plugin = registry.get("time")
    if time_plugin:
        result = await time_plugin.execute({"format": "datetime"})
        print(f"\n时间插件:")
        print(f"  成功: {result.success}")
        print(f"  消息: {result.message}")
        print(f"  数据: {result.data}")
    
    # 测试计算器插件
    calc_plugin = registry.get("calculator")
    if calc_plugin:
        result = await calc_plugin.execute({"expression": "1 + 2 * 3"})
        print(f"\n计算器插件:")
        print(f"  成功: {result.success}")
        print(f"  消息: {result.message}")
        print(f"  数据: {result.data}")
    
    # 测试搜索插件
    search_plugin = registry.get("search")
    if search_plugin:
        result = await search_plugin.execute({"query": "Python", "limit": 2})
        print(f"\n搜索插件:")
        print(f"  成功: {result.success}")
        print(f"  消息: {result.message}")
        print(f"  结果数: {result.data.get('results_count', 0)}")
    
    print()


async def test_preset_engine_with_tools():
    """测试 PresetEngine 工具调用"""
    print("=" * 50)
    print("测试2: PresetEngine 工具调用")
    print("=" * 50)
    
    async with AsyncSessionLocal() as db:
        engine = PresetEngine(db)
        
        # 获取默认预设
        try:
            preset = await engine.load_preset("default")
            print(f"\n加载预设: {preset.preset_name}")
            print(f"  模型: {preset.selected_model}")
            print(f"  插件: {preset.selected_plugins}")
            
            # 获取预设详情（包含可用工具）
            detail = await engine.get_preset_detail("default")
            print(f"\n可用工具:")
            for tool in detail.get("available_tools", []):
                print(f"  - {tool['name']}: {tool['description'][:50]}...")
            
        except ValueError as e:
            print(f"预设加载失败: {e}")
            print("请确保数据库已初始化并有默认预设")
            return
        
        # 测试工具调用对话（需要实际调用LLM，可选）
        print("\n" + "-" * 50)
        print("测试对话（无工具）:")
        print("-" * 50)
        
        message = "你好"
        print(f"用户: {message}")
        print("AI: ", end="", flush=True)
        
        try:
            response_chunks = []
            async for chunk in engine.chat(
                preset_id="default",
                message=message,
                history=[],
                stream=False,
                enable_tools=False  # 禁用工具，纯对话
            ):
                response_chunks.append(chunk)
                print(chunk, end="", flush=True)
            
            print()  # 换行
            
        except Exception as e:
            print(f"\n对话失败: {e}")
            print("（这是正常的，如果没有配置有效的模型API密钥）")


async def test_tool_adapter():
    """测试工具适配器"""
    print("\n" + "=" * 50)
    print("测试3: 工具适配器")
    print("=" * 50)
    
    from app.plugins.tool_adapter import ToolCallingManager, create_tool_from_plugin
    
    # 测试单个插件转 Tool
    tool = create_tool_from_plugin("time")
    if tool:
        print(f"\n时间插件转 Tool:")
        print(f"  名称: {tool.name}")
        print(f"  描述: {tool.description[:100]}...")
        
        # 测试执行
        result = await tool.ainvoke({"params": {"format": "time"}})
        print(f"  执行结果: {result}")
    
    # 测试 ToolCallingManager
    manager = ToolCallingManager({
        "selected_plugins": ["time", "calculator"]
    })
    
    print(f"\nToolCallingManager:")
    print(f"  有工具: {manager.has_tools()}")
    print(f"  工具数量: {len(manager.get_tools())}")
    print(f"  工具列表: {[t.name for t in manager.get_tools()]}")


async def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("HAXAtom 工具调用测试")
    print("=" * 60 + "\n")
    
    # 初始化插件
    await init_plugins()
    
    # 测试直接执行插件
    await test_direct_plugin_execution()
    
    # 测试工具适配器
    await test_tool_adapter()
    
    # 测试 PresetEngine（需要数据库）
    print("\n" + "=" * 50)
    print("测试4: PresetEngine 集成测试")
    print("=" * 50)
    print("（需要数据库连接和有效模型配置）")
    
    try:
        await test_preset_engine_with_tools()
    except Exception as e:
        print(f"\nPresetEngine 测试失败: {e}")
        print("请确保:")
        print("  1. 数据库已初始化并运行")
        print("  2. 有默认预设方案")
        print("  3. 模型配置正确且API密钥有效")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
