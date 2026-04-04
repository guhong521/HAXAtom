"""
知识库 Schema

知识库相关的 Pydantic 模型定义
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ==================== 知识库 Schema ====================

class KnowledgeBaseCreate(BaseModel):
    """创建知识库请求"""
    kb_name: str = Field(..., min_length=1, max_length=128, description="知识库名称")
    description: Optional[str] = Field(default=None, description="知识库描述")
    embedding_model: str = Field(..., description="嵌入模型ID（从模型配置中选择）")
    chunk_size: int = Field(default=500, ge=100, le=2000, description="分块大小")
    chunk_overlap: int = Field(default=50, ge=0, le=500, description="分块重叠大小")


class KnowledgeBaseUpdate(BaseModel):
    """更新知识库请求"""
    kb_name: Optional[str] = Field(default=None, min_length=1, max_length=128)
    description: Optional[str] = Field(default=None)
    chunk_size: Optional[int] = Field(default=None, ge=100, le=2000)
    chunk_overlap: Optional[int] = Field(default=None, ge=0, le=500)
    is_active: Optional[bool] = Field(default=None)


class KnowledgeBaseResponse(BaseModel):
    """知识库响应"""
    kb_id: str
    kb_name: str
    description: Optional[str]
    embedding_model: str
    chunk_size: int
    chunk_overlap: int
    storage_path: str
    document_count: int
    total_chunks: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class KnowledgeBaseList(BaseModel):
    """知识库列表项"""
    kb_id: str
    kb_name: str
    description: Optional[str]
    embedding_model: str
    document_count: int
    total_chunks: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 文档 Schema ====================

class DocumentCreate(BaseModel):
    """创建文档请求"""
    filename: str = Field(..., description="文件名")
    file_type: str = Field(..., description="文件类型 (txt, md, pdf, docx)")


class DocumentResponse(BaseModel):
    """文档响应"""
    doc_id: str
    kb_id: str
    filename: str
    file_type: str
    file_size: int
    status: str
    chunk_count: int
    error_message: Optional[str]
    meta_data: Optional[dict]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DocumentList(BaseModel):
    """文档列表项"""
    doc_id: str
    filename: str
    file_type: str
    file_size: int
    status: str
    chunk_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 检索 Schema ====================

class SearchRequest(BaseModel):
    """检索请求"""
    query: str = Field(..., min_length=1, description="查询文本")
    top_k: int = Field(default=5, ge=1, le=20, description="返回结果数量")
    score_threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="相似度阈值")


class SearchResult(BaseModel):
    """检索结果"""
    content: str = Field(..., description="文本内容")
    source: str = Field(..., description="来源文档")
    score: float = Field(..., description="相似度分数")
    metadata: dict = Field(default_factory=dict, description="元数据")


class SearchResponse(BaseModel):
    """检索响应"""
    query: str
    results: List[SearchResult]
    total: int
