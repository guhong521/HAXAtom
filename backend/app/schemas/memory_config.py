"""
记忆配置 Schema

记忆配置相关的 Pydantic 模型定义
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class MemoryConfigCreate(BaseModel):
    """创建记忆配置请求"""
    memory_name: str = Field(..., min_length=1, max_length=128, description="记忆配置名称")
    memory_type: str = Field(
        default="buffer_window",
        description="记忆类型: buffer_window(滑动窗口), summary(摘要), token_buffer(Token限制)"
    )
    memory_params: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="记忆参数"
    )


class MemoryConfigUpdate(BaseModel):
    """更新记忆配置请求"""
    memory_name: Optional[str] = Field(default=None, max_length=128)
    memory_type: Optional[str] = Field(default=None)
    memory_params: Optional[Dict[str, Any]] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)


class MemoryConfigResponse(BaseModel):
    """记忆配置响应"""
    memory_id: str
    memory_name: str
    memory_type: str
    memory_params: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MemoryConfigList(BaseModel):
    """记忆配置列表项"""
    memory_id: str
    memory_name: str
    memory_type: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
