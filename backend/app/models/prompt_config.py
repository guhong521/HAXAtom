"""
提示词配置表

存储人设、系统提示词的独立配置
"""

from typing import Optional, List

from sqlalchemy import JSON, Boolean, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PromptConfig(Base):
    """
    提示词配置表
    
    存储所有人设、系统提示词的独立配置
    """
    
    __tablename__ = "prompt_configs"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    prompt_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    prompt_name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 描述
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    variables: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True, default=list)
    temperature_override: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # 工具配置 - 存储选中的工具ID列表
    selected_tools: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True, default=list)
    use_all_tools: Mapped[bool] = mapped_column(Boolean, default=True)  # 是否使用全部工具
    # 预设对话 - 存储预设对话列表
    preset_dialogues: Mapped[Optional[List[dict]]] = mapped_column(JSON, nullable=True, default=list)
    
    def __repr__(self) -> str:
        return f"<PromptConfig(prompt_id='{self.prompt_id}')>"
