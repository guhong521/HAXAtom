"""
模型配置表

存储大模型（LLM/Embedding）的配置信息
"""

from typing import List, Optional

from sqlalchemy import JSON, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ModelConfig(Base):
    """
    模型配置表
    
    存储所有大模型的独立配置，每个模型为一个原子化条目
    支持一个厂商配置多个模型（如 glm-4, glm-5）
    """
    
    __tablename__ = "model_configs"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    model_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    model_name: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    model_type: Mapped[str] = mapped_column(String(32), nullable=False, default="chat")
    provider: Mapped[str] = mapped_column(String(32), nullable=False)
    api_base: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    api_key: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    default_params: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    disabled_models: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True, default=list)
    
    def __repr__(self) -> str:
        return f"<ModelConfig(model_id='{self.model_id}', provider='{self.provider}')>"
