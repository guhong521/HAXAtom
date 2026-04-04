"""
测试对话 API

测试 LangGraph 工作流的对话接口
"""

import json
import urllib.request
import urllib.error


def test_chat_api():
    """测试对话接口"""
    url = "http://localhost:8000/api/v1/chat/completions"
    
    data = {
        "preset_id": "test_preset",
        "message": "你好，请介绍一下自己",
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = response.read().decode('utf-8')
            print("=" * 60)
            print("对话接口响应:")
            print("=" * 60)
            print(result)
            print("=" * 60)
            
            # 解析响应
            resp_data = json.loads(result)
            if resp_data.get("code") == 200:
                print("[SUCCESS] 对话接口测试通过!")
                print(f"AI回复: {resp_data.get('data', {}).get('content', '无内容')[:100]}...")
            else:
                print(f"[ERROR] 对话接口返回错误: {resp_data.get('message')}")
                
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP错误: {e.code}")
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f"[ERROR] 请求失败: {e}")


if __name__ == "__main__":
    print("测试 LangGraph 对话接口...")
    print("预设ID: test_preset")
    print("消息: 你好，请介绍一下自己")
    print()
    test_chat_api()
