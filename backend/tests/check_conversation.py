"""
检查对话历史是否正确保存
"""

import asyncio
import sys
sys.path.insert(0, 'f:\\2025python\\HAXAtom\\backend')

from app.db.session import AsyncSessionLocal
from app.services.conversation_service import ConversationService


async def check_conversation():
    """检查会话历史"""
    print("=" * 60)
    print("检查会话历史")
    print("=" * 60)
    
    async with AsyncSessionLocal() as session:
        conv_service = ConversationService(session)
        
        # 检查测试会话
        session_id = "memory_api_test_001"
        conversation = await conv_service.get_conversation(session_id)
        
        if conversation:
            print(f"会话ID: {conversation.session_id}")
            print(f"消息数量: {conversation.message_count}")
            print(f"消息列表类型: {type(conversation.messages)}")
            print(f"消息列表: {conversation.messages}")
        else:
            print(f"会话不存在: {session_id}")


if __name__ == "__main__":
    asyncio.run(check_conversation())
