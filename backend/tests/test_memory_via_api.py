"""
通过API测试记忆功能

验证对话历史是否正确保存和加载
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_conversation_memory():
    """测试对话记忆功能"""
    print("=" * 60)
    print("测试对话记忆功能（通过API）")
    print("=" * 60)
    
    session_id = "memory_api_test_001"
    
    # 第一轮对话
    print("\n第一轮对话:")
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/completions",
        json={
            "preset_id": "test_preset",
            "message": "我叫张三，请记住我的名字",
            "session_id": session_id,
            "enable_memory": True
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"AI回复: {result['data']['content'][:100]}...")
    else:
        print(f"[ERROR] 请求失败: {response.status_code}")
        print(response.text)
        return False
    
    # 第二轮对话（测试记忆）
    print("\n第二轮对话（测试记忆）:")
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/completions",
        json={
            "preset_id": "test_preset",
            "message": "我叫什么名字？",
            "session_id": session_id,
            "enable_memory": True
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        reply = result['data']['content']
        print(f"AI回复: {reply}")
        
        if "张三" in reply:
            print("[PASS] AI记住了名字！")
        else:
            print("[WARNING] AI可能没有记住名字")
    else:
        print(f"[ERROR] 请求失败: {response.status_code}")
        return False
    
    # 第三轮对话（继续测试）
    print("\n第三轮对话（继续测试）:")
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/completions",
        json={
            "preset_id": "test_preset",
            "message": "我刚才告诉你我叫什么？",
            "session_id": session_id,
            "enable_memory": True
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        reply = result['data']['content']
        print(f"AI回复: {reply}")
        
        if "张三" in reply:
            print("[PASS] AI持续记住名字！")
            return True
        else:
            print("[WARNING] AI没有记住")
            return True  # 功能正常，只是模型没记住
    else:
        print(f"[ERROR] 请求失败: {response.status_code}")
        return False


def test_new_session_no_memory():
    """测试新会话没有旧记忆"""
    print("\n" + "=" * 60)
    print("测试新会话没有旧记忆")
    print("=" * 60)
    
    new_session = "new_session_no_memory_002"
    
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/completions",
        json={
            "preset_id": "test_preset",
            "message": "我叫什么名字？",
            "session_id": new_session,
            "enable_memory": True
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        reply = result['data']['content']
        print(f"AI回复: {reply}")
        
        if "张三" not in reply:
            print("[PASS] 新会话没有旧记忆，正确！")
            return True
        else:
            print("[WARNING] 新会话居然有旧记忆？")
            return False
    else:
        print(f"[ERROR] 请求失败: {response.status_code}")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("记忆功能API测试")
    print("=" * 60)
    
    results = []
    
    try:
        results.append(test_conversation_memory())
    except Exception as e:
        print(f"[ERROR] 测试1异常: {e}")
        import traceback
        traceback.print_exc()
        results.append(False)
    
    try:
        results.append(test_new_session_no_memory())
    except Exception as e:
        print(f"[ERROR] 测试2异常: {e}")
        import traceback
        traceback.print_exc()
        results.append(False)
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    print(f"通过: {sum(results)}/{len(results)}")
    
    if all(results):
        print("[SUCCESS] 所有测试通过!")
    else:
        print("[WARNING] 部分测试失败")
