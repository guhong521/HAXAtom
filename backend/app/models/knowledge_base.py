"""
知识库表

存储知识库配置和文档信息
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class KnowledgeBase(Base):
    """
    知识库表
    
    存储知识库的基本配置信息
    """
    
    __tablename__ = "knowledge_bases"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kb_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    kb_name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # 关联的嵌入模型（从模型配置中选择）
    embedding_model: Mapped[str] = mapped_column(String(64), nullable=False)
    
    # 分块配置
    chunk_size: Mapped[int] = mapped_column(Integer, default=500)
    chunk_overlap: Mapped[int] = mapped_column(Integer, default=50)
    
    # 存储路径
    storage_path: Mapped[str] = mapped_column(String(256), nullable=False)
    
    # 文档数量统计
    document_count: Mapped[int] = mapped_column(Integer, default=0)
    total_chunks: Mapped[int] = mapped_column(Integer, default=0)
    
    # 状态
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联文档
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="knowledge_base", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<KnowledgeBase(kb_id='{self.kb_id}', name='{self.kb_name}')>"


class Document(Base):
    """
    文档表
    
    存储上传的文档信息
    """
    
    __tablename__ = "documents"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    doc_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    kb_id: Mapped[str] = mapped_column(String(64), ForeignKey("knowledge_bases.kb_id"), nullable=False)
    
    # 文档信息
    filename: Mapped[str] = mapped_column(String(256), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_type: Mapped[str] = mapped_column(String(32), nullable=False)  # pdf, txt, md, etc.
    file_size: Mapped[int] = mapped_column(Integer, default=0)  # bytes
    
    # 处理状态
    status: Mapped[str] = mapped_column(String(32), default="pending")  # pending, processing, completed, failed
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # 元数据
    meta_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
    
    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联
    knowledge_base: Mapped["KnowledgeBase"] = relationship("KnowledgeBase", back_populates="documents")
    
    def __repr__(self) -> str:
        return f"<Document(doc_id='{self.doc_id}', filename='{self.filename}')>"
