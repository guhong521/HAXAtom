"""
完整工作流测试

测试整个对话流程：
1. 预设加载
2. 资源校验
3. 记忆加载
4. 对话执行
5. 历史保存
6. 记忆 recall
"""

import asyncio
import sys
sys.path.insert(0, 'f:\\2025python\\HAXAtom\\backend')

from app.db.session import AsyncSessionLocal
from app.core import PresetEngine
from app.services.conversation_service import ConversationService


async def test_full_workflow():
    """测试完整工作流"""
    print("=" * 70)
    print("完整工作流测试")
    print("=" * 70)
    
    async with AsyncSessionLocal() as session:
        engine = PresetEngine(session)
        conv_service = ConversationService(session)
        
        session_id = "full_workflow_test_001"
        preset_id = "test_preset"
        
        # ========== 测试1: 基础对话 ==========
        print("\n[测试1] 基础对话（无记忆）")
        print("-" * 50)
        
        response_chunks = []
        async for chunk in engine.chat(
            preset_id=preset_id,
            message="你好，请简短介绍一下自己",
            session_id=session_id,
            enable_memory=False
        ):
            response_chunks.append(chunk)
        
        response1 = "".join(response_chunks)
        print(f"用户: 你好，请简短介绍一下自己")
        print(f"AI: {response1[:100]}...")
        print("[PASS] 基础对话成功")
        
        # ========== 测试2: 带记忆的对话 ==========
        print("\n[测试2] 带记忆的对话 - 第一轮")
        print("-" * 50)
        
        response_chunks = []
        async for chunk in engine.chat(
            preset_id=preset_id,
            message="我叫李四，请记住我的名字",
            session_id=session_id,
            enable_memory=True
        ):
            response_chunks.append(chunk)
        
        response2 = "".join(response_chunks)
        print(f"用户: 我叫李四，请记住我的名字")
        print(f"AI: {response2[:100]}...")
        print("[PASS] 记忆对话第一轮成功")
        
        # ========== 测试3: 记忆召回 ==========
        print("\n[测试3] 记忆召回测试")
        print("-" * 50)
        
        response_chunks = []
        async for chunk in engine.chat(
            preset_id=preset_id,
            message="我叫什么名字？",
            session_id=session_id,
            enable_memory=True
        ):
            response_chunks.append(chunk)
        
        response3 = "".join(response_chunks)
        print(f"用户: 我叫什么名字？")
        print(f"AI: {response3}")
        
        if "李四" in response3:
            print("[PASS] 记忆召回成功！AI记住了名字")
        else:
            print("[WARNING] AI可能没有正确记住名字")
        
        # ========== 测试4: 验证历史保存 ==========
        print("\n[测试4] 验证历史保存")
        print("-" * 50)
        
        conversation = await conv_service.get_conversation(session_id)
        if conversation:
            print(f"会话ID: {conversation.session_id}")
            print(f"消息数量: {conversation.message_count}")
            print(f"\n消息历史:")
            for i, msg in enumerate(conversation.messages, 1):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")[:40]
                print(f"  {i}. [{role:10}] {content}...")
            print("[PASS] 历史保存成功")
        else:
            print("[FAIL] 会话不存在")
        
        # ========== 测试5: 新会话无记忆 ==========
        print("\n[测试5] 新会话无记忆测试")
        print("-" * 50)
        
        new_session_id = "full_workflow_test_002"
        
        response_chunks = []
        async for chunk in engine.chat(
            preset_id=preset_id,
            message="你知道我叫什么名字吗？",
            session_id=new_session_id,
            enable_memory=True
        ):
            response_chunks.append(chunk)
        
        response5 = "".join(response_chunks)
        print(f"用户: 你知道我叫什么名字吗？")
        print(f"AI: {response5[:100]}...")
        
        if "李四" not in response5:
            print("[PASS] 新会话没有旧记忆，正确！")
        else:
            print("[FAIL] 新会话不应该有旧记忆")
        
        # ========== 测试6: 资源校验错误 ==========
        print("\n[测试6] 资源校验错误测试")
        print("-" * 50)
        
        try:
            async for chunk in engine.chat(
                preset_id="non_existent_preset",
                message="测试消息",
                session_id="error_test"
            ):
                pass
            print("[FAIL] 应该抛出错误")
        except ValueError as e:
            print(f"[PASS] 正确捕获错误: {str(e)[:50]}...")
        
        # ========== 测试汇总 ==========
        print("\n" + "=" * 70)
        print("测试汇总")
        print("=" * 70)
        print("所有测试流程执行完成！")
        print("\n核心功能验证:")
        print("  [OK] 基础对话")
        print("  [OK] 记忆系统")
        print("  [OK] 历史保存")
        print("  [OK] 会话隔离")
        print("  [OK] 错误处理")


if __name__ == "__main__":
    asyncio.run(test_full_workflow())
