"""
记忆配置表

存储记忆策略的独立配置
"""

from typing import Optional

from sqlalchemy import JSON, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class MemoryConfig(Base):
    """
    记忆配置表
    
    存储所有记忆策略的独立配置
    """
    
    __tablename__ = "memory_configs"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    memory_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    memory_name: Mapped[str] = mapped_column(String(128), nullable=False)
    memory_type: Mapped[str] = mapped_column(String(32), nullable=False)
    memory_params: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    def __repr__(self) -> str:
        return f"<MemoryConfig(memory_id='{self.memory_id}', type='{self.memory_type}')>"
