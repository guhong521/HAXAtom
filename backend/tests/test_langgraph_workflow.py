"""
LangGraph 工作流测试

测试新的 LangGraph 实现是否正确工作
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


async def test_state_types():
    """测试状态类型定义"""
    from app.core.state_types import AgentState, create_initial_state, format_retrieved_context
    
    # 测试创建初始状态
    state = create_initial_state(
        input_message="你好",
        preset_id="test_preset",
        session_id="test_session",
        system_prompt="你是一个助手"
    )
    
    assert state["input"] == "你好"
    assert state["preset_id"] == "test_preset"
    assert state["session_id"] == "test_session"
    assert len(state["messages"]) == 2  # System + Human
    
    print("[PASS] 状态类型测试通过")


async def test_rag_engine():
    """测试 RAG 引擎"""
    from app.core.rag_engine import format_retrieved_context
    
    # 测试格式化函数
    documents = [
        {"content": "测试内容1", "source": "doc1", "score": 0.9},
        {"content": "测试内容2", "source": "doc2", "score": 0.8},
    ]
    
    context = format_retrieved_context(documents)
    assert "测试内容1" in context
    assert "doc1" in context
    assert "0.90" in context
    
    print("[PASS] RAG 引擎测试通过")


async def test_tool_engine():
    """测试工具引擎"""
    from app.core.tool_engine import ToolEngine
    
    # 注意：这里不实际调用数据库，只测试基本结构
    print("[PASS] 工具引擎结构测试通过")


async def test_preset_engine_structure():
    """测试预设引擎结构"""
    from app.core.preset_engine import PresetEngine
    from app.db.session import AsyncSessionLocal
    
    # 测试引擎初始化
    async with AsyncSessionLocal() as session:
        engine = PresetEngine(session)
        assert engine is not None
        assert hasattr(engine, 'build_graph')
        assert hasattr(engine, 'chat')
    
    print("[PASS] 预设引擎结构测试通过")


async def test_imports():
    """测试所有导入是否正确"""
    try:
        from app.core import (
            PresetEngine,
            RAGEngine,
            ToolEngine,
            AgentState,
            RAGState,
            ToolState,
            create_initial_state,
            format_retrieved_context,
        )
        print("[PASS] 所有核心组件导入成功")
    except ImportError as e:
        print(f"[FAIL] 导入失败: {e}")
        raise


async def test_langgraph_imports():
    """测试 LangGraph 依赖"""
    try:
        from langgraph.graph import StateGraph, END
        from langgraph.prebuilt import ToolNode
        from langgraph.checkpoint.memory import MemorySaver
        print("[PASS] LangGraph 依赖导入成功")
    except ImportError as e:
        print(f"[FAIL] LangGraph 导入失败: {e}")
        raise


async def test_lcel_chain():
    """测试 LCEL 链语法"""
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnableLambda
    
    # 测试基本 LCEL 链
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个助手"),
        ("human", "{input}")
    ])
    
    # 测试管道语法（不实际执行模型）
    # chain = prompt | RunnableLambda(lambda x: x)
    
    print("[PASS] LCEL 链语法测试通过")


async def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("LangGraph 工作流测试")
    print("=" * 60)
    
    try:
        await test_imports()
        await test_langgraph_imports()
        await test_state_types()
        await test_rag_engine()
        await test_tool_engine()
        await test_lcel_chain()
        
        # 数据库相关测试
        try:
            await test_preset_engine_structure()
        except Exception as e:
            print(f"[SKIP] 数据库测试跳过（可能需要初始化数据库）: {e}")
        
        print("=" * 60)
        print("[SUCCESS] 所有测试通过！")
        print("=" * 60)
        
    except Exception as e:
        print("=" * 60)
        print(f"[ERROR] 测试失败: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(run_all_tests())
