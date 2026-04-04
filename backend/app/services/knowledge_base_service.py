"""
知识库服务

提供知识库的完整管理功能：
- 知识库 CRUD
- 文档上传和存储
- 文档分块和向量化
- 向量检索
"""

import os
import shutil
import uuid
from pathlib import Path
from typing import List, Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Document, KnowledgeBase
from app.schemas.knowledge_base import (
    DocumentCreate,
    DocumentResponse,
    KnowledgeBaseCreate,
    KnowledgeBaseResponse,
    KnowledgeBaseUpdate,
)


class KnowledgeBaseService:
    """
    知识库服务类
    
    管理知识库的生命周期和所有操作
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        # 知识库存储根目录
        self.storage_root = Path("data/knowledge")
        self.storage_root.mkdir(parents=True, exist_ok=True)
    
    # ==================== 知识库管理 ====================
    
    async def create_knowledge_base(
        self,
        data: KnowledgeBaseCreate
    ) -> KnowledgeBase:
        """
        创建知识库
        
        Args:
            data: 知识库创建数据
            
        Returns:
            KnowledgeBase: 创建的知识库对象
        """
        # 生成唯一ID
        kb_id = f"kb_{uuid.uuid4().hex[:8]}"
        
        # 创建存储目录
        storage_path = self.storage_root / kb_id
        storage_path.mkdir(parents=True, exist_ok=True)
        
        # 创建知识库记录
        kb = KnowledgeBase(
            kb_id=kb_id,
            kb_name=data.kb_name,
            description=data.description,
            embedding_model=data.embedding_model,
            chunk_size=data.chunk_size,
            chunk_overlap=data.chunk_overlap,
            storage_path=str(storage_path),
        )
        
        self.db.add(kb)
        await self.db.commit()
        await self.db.refresh(kb)
        
        return kb
    
    async def get_knowledge_base(self, kb_id: str) -> Optional[KnowledgeBase]:
        """
        获取知识库
        
        Args:
            kb_id: 知识库ID
            
        Returns:
            Optional[KnowledgeBase]: 知识库对象或None
        """
        result = await self.db.execute(
            select(KnowledgeBase).where(
                KnowledgeBase.kb_id == kb_id,
                KnowledgeBase.is_active == True
            )
        )
        return result.scalar_one_or_none()
    
    async def list_knowledge_bases(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[KnowledgeBase]:
        """
        获取知识库列表
        
        Args:
            skip: 跳过数量
            limit: 返回数量限制
            
        Returns:
            List[KnowledgeBase]: 知识库列表
        """
        result = await self.db.execute(
            select(KnowledgeBase)
            .where(KnowledgeBase.is_active == True)
            .order_by(KnowledgeBase.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def update_knowledge_base(
        self,
        kb_id: str,
        data: KnowledgeBaseUpdate
    ) -> Optional[KnowledgeBase]:
        """
        更新知识库
        
        Args:
            kb_id: 知识库ID
            data: 更新数据
            
        Returns:
            Optional[KnowledgeBase]: 更新后的知识库对象
        """
        kb = await self.get_knowledge_base(kb_id)
        if not kb:
            return None
        
        # 更新字段
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(kb, field, value)
        
        await self.db.commit()
        await self.db.refresh(kb)
        
        return kb
    
    async def delete_knowledge_base(self, kb_id: str) -> bool:
        """
        删除知识库（软删除）
        
        Args:
            kb_id: 知识库ID
            
        Returns:
            bool: 是否成功删除
        """
        kb = await self.get_knowledge_base(kb_id)
        if not kb:
            return False
        
        # 软删除
        kb.is_active = False
        await self.db.commit()
        
        return True
    
    # ==================== 文档管理 ====================
    
    async def upload_document(
        self,
        kb_id: str,
        filename: str,
        content: bytes,
        file_type: str
    ) -> Document:
        """
        上传文档到知识库
        
        Args:
            kb_id: 知识库ID
            filename: 文件名
            content: 文件内容（二进制）
            file_type: 文件类型
            
        Returns:
            Document: 创建的文档对象
        """
        # 获取知识库
        kb = await self.get_knowledge_base(kb_id)
        if not kb:
            raise ValueError(f"Knowledge base '{kb_id}' not found")
        
        # 生成文档ID
        doc_id = f"doc_{uuid.uuid4().hex[:8]}"
        
        # 保存文件
        storage_path = Path(kb.storage_path)
        file_path = storage_path / f"{doc_id}_{filename}"
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 创建文档记录
        doc = Document(
            doc_id=doc_id,
            kb_id=kb_id,
            filename=filename,
            file_path=str(file_path),
            file_type=file_type,
            file_size=len(content),
            status="pending",
        )
        
        self.db.add(doc)
        
        # 更新知识库文档计数
        kb.document_count += 1
        
        await self.db.commit()
        await self.db.refresh(doc)
        
        return doc
    
    async def get_document(self, doc_id: str) -> Optional[Document]:
        """
        获取文档
        
        Args:
            doc_id: 文档ID
            
        Returns:
            Optional[Document]: 文档对象或None
        """
        result = await self.db.execute(
            select(Document).where(Document.doc_id == doc_id)
        )
        return result.scalar_one_or_none()
    
    async def list_documents(
        self,
        kb_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Document]:
        """
        获取知识库的文档列表
        
        Args:
            kb_id: 知识库ID
            skip: 跳过数量
            limit: 返回数量限制
            
        Returns:
            List[Document]: 文档列表
        """
        result = await self.db.execute(
            select(Document)
            .where(Document.kb_id == kb_id)
            .order_by(Document.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def delete_document(self, doc_id: str) -> bool:
        """
        删除文档
        
        Args:
            doc_id: 文档ID
            
        Returns:
            bool: 是否成功删除
        """
        doc = await self.get_document(doc_id)
        if not doc:
            return False
        
        # 删除文件
        try:
            if os.path.exists(doc.file_path):
                os.remove(doc.file_path)
        except Exception as e:
            print(f"[KnowledgeBaseService] Failed to delete file: {e}")
        
        # 更新知识库文档计数
        kb = await self.get_knowledge_base(doc.kb_id)
        if kb and kb.document_count > 0:
            kb.document_count -= 1
        
        # 删除数据库记录
        await self.db.delete(doc)
        await self.db.commit()
        
        return True
    
    # ==================== 文档处理 ====================
    
    async def process_document(self, doc_id: str) -> bool:
        """
        处理文档（分块和向量化）
        
        Args:
            doc_id: 文档ID
            
        Returns:
            bool: 是否成功处理
        """
        doc = await self.get_document(doc_id)
        if not doc:
            return False
        
        try:
            # 更新状态为处理中
            doc.status = "processing"
            await self.db.commit()
            
            # 获取知识库配置
            kb = await self.get_knowledge_base(doc.kb_id)
            if not kb:
                raise ValueError(f"Knowledge base '{doc.kb_id}' not found")
            
            # 读取文档内容
            text = await self._extract_text(doc.file_path, doc.file_type)
            if not text:
                raise ValueError("Failed to extract text from document")
            
            # 分块
            chunks = self._split_text(
                text,
                chunk_size=kb.chunk_size,
                chunk_overlap=kb.chunk_overlap
            )
            
            # 向量化并存储到 ChromaDB
            from app.services.vector_store_service import VectorStoreService
            vector_service = VectorStoreService(self.db)
            
            success = await vector_service.add_documents(
                kb_id=kb.kb_id,
                doc_id=doc.doc_id,
                chunks=chunks,
                embedding_model_id=kb.embedding_model
            )
            
            if not success:
                raise ValueError("Failed to vectorize and store documents")
            
            # 更新文档块数
            doc.chunk_count = len(chunks)
            doc.status = "completed"
            
            # 更新知识库总块数
            kb.total_chunks += len(chunks)
            
            await self.db.commit()
            
            return True
            
        except Exception as e:
            doc.status = "failed"
            doc.error_message = str(e)
            await self.db.commit()
            print(f"[KnowledgeBaseService] Failed to process document: {e}")
            return False
    
    async def _extract_text(self, file_path: str, file_type: str) -> str:
        """
        从文件中提取文本
        
        Args:
            file_path: 文件路径
            file_type: 文件类型
            
        Returns:
            str: 提取的文本
        """
        file_type = file_type.lower()
        
        if file_type == "txt" or file_type == "md":
            # 文本文件直接读取
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        
        elif file_type == "pdf":
            # PDF 文件使用 PyPDF2 或 pdfplumber
            try:
                import pdfplumber
                text = ""
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() or ""
                return text
            except ImportError:
                raise ImportError("pdfplumber is required for PDF processing. Install with: pip install pdfplumber")
        
        elif file_type in ["docx", "doc"]:
            # Word 文档
            try:
                import docx2txt
                return docx2txt.process(file_path)
            except ImportError:
                raise ImportError("docx2txt is required for Word processing. Install with: pip install docx2txt")
        
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _split_text(
        self,
        text: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ) -> List[str]:
        """
        将文本分块
        
        Args:
            text: 原始文本
            chunk_size: 块大小
            chunk_overlap: 重叠大小
            
        Returns:
            List[str]: 文本块列表
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", "；", " ", ""]
        )
        
        return splitter.split_text(text)
    
    # ==================== 检索功能 ====================
    
    async def search(
        self,
        kb_id: str,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.5
    ) -> List[dict]:
        """
        在知识库中检索相关内容
        
        Args:
            kb_id: 知识库ID
            query: 查询文本
            top_k: 返回结果数量
            score_threshold: 相似度阈值
            
        Returns:
            List[dict]: 检索结果
        """
        # 获取知识库
        kb = await self.get_knowledge_base(kb_id)
        if not kb:
            raise ValueError(f"Knowledge base '{kb_id}' not found")
        
        # 使用向量存储服务检索
        from app.services.vector_store_service import VectorStoreService
        vector_service = VectorStoreService(self.db)
        
        results = await vector_service.search(
            kb_id=kb_id,
            query=query,
            embedding_model_id=kb.embedding_model,
            top_k=top_k,
            score_threshold=score_threshold
        )
        
        return results
