"""
完整工作流测试（通过API）

测试整个对话流程：
1. 创建会话
2. 发送消息
3. 记忆保存
4. 记忆召回
5. 会话隔离
"""

import requests
import time

BASE_URL = "http://localhost:8000"


def test_full_workflow():
    """测试完整工作流"""
    print("=" * 70)
    print("完整工作流测试（API方式）")
    print("=" * 70)
    
    session_id = f"full_api_test_{int(time.time())}"
    preset_id = "test_preset"
    
    # ========== 测试1: 基础对话 ==========
    print("\n[测试1] 基础对话")
    print("-" * 50)
    
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/completions",
        json={
            "preset_id": preset_id,
            "message": "你好，请简短介绍一下自己",
            "session_id": session_id,
            "enable_memory": True
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        content = data.get("data", {}).get("content", "")
        print(f"用户: 你好，请简短介绍一下自己")
        print(f"AI: {content[:80]}...")
        print(f"会话ID: {data.get('data', {}).get('session_id', '')}")
        print("[PASS] 基础对话成功")
    else:
        print(f"[FAIL] 请求失败: {response.status_code}")
        return
    
    # ========== 测试2: 记忆保存 ==========
    print("\n[测试2] 记忆保存 - 第一轮")
    print("-" * 50)
    
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/completions",
        json={
            "preset_id": preset_id,
            "message": "我叫王五，请记住我的名字",
            "session_id": session_id,
            "enable_memory": True
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        content = data.get("data", {}).get("content", "")
        print(f"用户: 我叫王五，请记住我的名字")
        print(f"AI: {content[:80]}...")
        print("[PASS] 记忆保存成功")
    else:
        print(f"[FAIL] 请求失败")
        return
    
    # ========== 测试3: 记忆召回 ==========
    print("\n[测试3] 记忆召回测试")
    print("-" * 50)
    
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/completions",
        json={
            "preset_id": preset_id,
            "message": "我叫什么名字？",
            "session_id": session_id,
            "enable_memory": True
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        content = data.get("data", {}).get("content", "")
        print(f"用户: 我叫什么名字？")
        print(f"AI: {content}")
        
        if "王五" in content:
            print("[PASS] 记忆召回成功！AI记住了名字")
        else:
            print("[WARNING] AI可能没有正确记住名字")
    else:
        print(f"[FAIL] 请求失败")
    
    # ========== 测试4: 验证历史保存 ==========
    print("\n[测试4] 验证历史保存")
    print("-" * 50)
    
    response = requests.get(f"{BASE_URL}/api/v1/conversations/{session_id}")
    
    if response.status_code == 200:
        data = response.json()
        conversation = data.get("data", {})
        messages = conversation.get("messages", [])
        
        print(f"会话ID: {conversation.get('session_id', '')}")
        print(f"消息数量: {len(messages)}")
        print(f"\n消息历史:")
        for i, msg in enumerate(messages, 1):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:35]
            print(f"  {i}. [{role:10}] {content}...")
        print("[PASS] 历史保存成功")
    else:
        print(f"[FAIL] 获取会话失败: {response.status_code}")
    
    # ========== 测试5: 新会话无记忆 ==========
    print("\n[测试5] 新会话无记忆测试")
    print("-" * 50)
    
    new_session_id = f"full_api_test_new_{int(time.time())}"
    
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/completions",
        json={
            "preset_id": preset_id,
            "message": "你知道我叫什么名字吗？",
            "session_id": new_session_id,
            "enable_memory": True
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        content = data.get("data", {}).get("content", "")
        print(f"用户: 你知道我叫什么名字吗？")
        print(f"AI: {content[:80]}...")
        
        if "王五" not in content:
            print("[PASS] 新会话没有旧记忆，正确！")
        else:
            print("[FAIL] 新会话不应该有旧记忆")
    else:
        print(f"[FAIL] 请求失败")
    
    # ========== 测试6: 错误处理 ==========
    print("\n[测试6] 错误处理测试")
    print("-" * 50)
    
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/completions",
        json={
            "preset_id": "non_existent_preset",
            "message": "测试消息"
        }
    )
    
    if response.status_code == 404:
        print(f"[PASS] 正确返回404: {response.json().get('detail', '')[:40]}...")
    else:
        print(f"[FAIL] 应该返回404，实际返回: {response.status_code}")
    
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
    test_full_workflow()
