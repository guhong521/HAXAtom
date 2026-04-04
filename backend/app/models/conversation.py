"""
对话历史表

存储对话会话和消息历史 - 支持多平台（Web、QQ、飞书等）
"""

from typing import List, Optional

from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Conversation(Base):
    """
    对话历史表 - 支持多平台
    
    存储来自不同平台的对话历史：
    - Web平台：网页聊天界面
    - QQ平台：QQ机器人（群聊/私聊）
    - Feishu平台：飞书机器人
    - DingTalk平台：钉钉机器人
    - Telegram平台：Telegram机器人
    """
    
    __tablename__ = "conversations"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # 会话标识
    session_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    
    # 平台标识（新增）
    channel_type: Mapped[str] = mapped_column(
        String(32),
        default="web",
        index=True,
        comment="平台类型: web, qq, qq_group, qq_private, feishu, dingtalk, telegram"
    )
    channel_id: Mapped[Optional[str]] = mapped_column(
        String(128),
        nullable=True,
        index=True,
        comment="平台特定ID: QQ号/群号、飞书用户ID等"
    )
    
    # 关联预设方案
    preset_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("presets.preset_id"),
        nullable=False
    )
    
    # 对话内容
    title: Mapped[str] = mapped_column(String(256), nullable=False, default="新对话")
    messages: Mapped[List[dict]] = mapped_column(JSON, nullable=False, default=list)
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # 平台特定配置（可选，用于存储平台特殊设置）
    platform_config: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        comment="平台特定配置，如QQ的群名片、飞书的部门信息等"
    )
    
    # 关系
    preset: Mapped["Preset"] = relationship("Preset", lazy="selectin")
    
    def __repr__(self) -> str:
        return f"<Conversation(channel='{self.channel_type}', session='{self.session_id}', messages={self.message_count})>"
