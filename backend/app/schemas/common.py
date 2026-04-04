"""
通用 Pydantic Schema

基础响应模型和通用字段定义
"""

from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field


class TimestampMixin(BaseModel):
    """时间戳混入类"""
    created_at: datetime
    updated_at: datetime


T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    """
    统一响应基类
    
    所有API响应遵循此格式
    """
    code: int = Field(default=200, description="状态码")
    message: str = Field(default="success", description="消息")
    data: Optional[T] = Field(default=None, description="数据")
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp()), description="时间戳")


class ListResponse(ResponseBase[List[T]], Generic[T]):
    """列表响应"""
    total: int = Field(default=0, description="总数")
    page: int = Field(default=1, description="当前页")
    page_size: int = Field(default=20, description="每页数量")


class PaginationParams(BaseModel):
    """分页参数"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页数量")


class IDResponse(BaseModel):
    """ID响应"""
    id: int


class CountResponse(BaseModel):
    """计数响应"""
    count: int
