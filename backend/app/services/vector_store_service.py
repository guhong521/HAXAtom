"""
向量存储服务

基于 ChromaDB 实现文档的向量存储和检索
支持多种嵌入模型（通过预设方案配置）
"""

import hashlib
from pathlib import Path
from typing import List, Optional

import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_core.documents import Document as LangchainDocument
from langchain_core.embeddings import Embeddings
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import KnowledgeBase, ModelConfig


class VectorStoreService:
    """
    向量存储服务
    
    管理 ChromaDB 向量数据库，提供文档向量化和检索功能
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        # ChromaDB 存储路径
        self.persist_directory = Path("data/vectordb")
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # 初始化 ChromaDB 客户端
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )
    
    async def get_embedding_model(self, model_id: str) -> Embeddings:
        """
        获取嵌入模型实例
        
        根据模型配置创建对应的 LangChain Embeddings
        
        Args:
            model_id: 模型配置ID
            
        Returns:
            Embeddings: LangChain 嵌入模型实例
        """
        # 查询模型配置
        result = await self.db.execute(
            select(ModelConfig).where(
                ModelConfig.model_id == model_id,
                ModelConfig.is_active == True
            )
        )
        model_config = result.scalar_one_or_none()
        
        if not model_config:
            raise ValueError(f"Embedding model '{model_id}' not found")
        
        if model_config.model_type != "embedding":
            raise ValueError(f"Model '{model_id}' is not an embedding model")
        
        # 根据提供商创建对应的嵌入模型
        provider = model_config.provider.lower()
        
        if provider == "zhipu":
            from langchain_community.embeddings import ZhipuAIEmbeddings
            return ZhipuAIEmbeddings(
                api_key=model_config.api_key,
                model=model_config.model_name,
            )
        
        elif provider == "openai":
            from langchain_openai import OpenAIEmbeddings
            return OpenAIEmbeddings(
                api_key=model_config.api_key,
                base_url=model_config.api_base,
                model=model_config.model_name,
            )
        
        elif provider == "ollama":
            from langchain_ollama import OllamaEmbeddings
            return OllamaEmbeddings(
                base_url=model_config.api_base or "http://localhost:11434",
                model=model_config.model_name,
            )
        
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")
    
    def _get_collection_name(self, kb_id: str) -> str:
        """
        获取知识库的集合名称
        
        Args:
            kb_id: 知识库ID
            
        Returns:
            str: 集合名称
        """
        # 使用知识库ID的哈希作为集合名（ChromaDB 集合名有长度限制）
        return f"kb_{hashlib.md5(kb_id.encode()).hexdigest()[:16]}"
    
    async def add_documents(
        self,
        kb_id: str,
        doc_id: str,
        chunks: List[str],
        embedding_model_id: str
    ) -> bool:
        """
        添加文档块到向量数据库
        
        Args:
            kb_id: 知识库ID
            doc_id: 文档ID
            chunks: 文本块列表
            embedding_model_id: 嵌入模型ID
            
        Returns:
            bool: 是否成功添加
        """
        try:
            # 获取嵌入模型
            embeddings = await self.get_embedding_model(embedding_model_id)
            
            # 创建 LangChain Documents
            documents = [
                LangchainDocument(
                    page_content=chunk,
                    metadata={
                        "doc_id": doc_id,
                        "chunk_index": i,
                        "kb_id": kb_id,
                    }
                )
                for i, chunk in enumerate(chunks)
            ]
            
            # 获取集合名称
            collection_name = self._get_collection_name(kb_id)
            
            # 创建或获取向量存储
            vector_store = Chroma(
                collection_name=collection_name,
                embedding_function=embeddings,
                persist_directory=str(self.persist_directory),
            )
            
            # 添加文档
            vector_store.add_documents(documents)
            
            return True
            
        except Exception as e:
            print(f"[VectorStoreService] Failed to add documents: {e}")
            return False
    
    async def search(
        self,
        kb_id: str,
        query: str,
        embedding_model_id: str,
        top_k: int = 5,
        score_threshold: float = 0.5
    ) -> List[dict]:
        """
        检索相似文档
        
        Args:
            kb_id: 知识库ID
            query: 查询文本
            embedding_model_id: 嵌入模型ID
            top_k: 返回结果数量
            score_threshold: 相似度阈值
            
        Returns:
            List[dict]: 检索结果列表
        """
        try:
            # 获取嵌入模型
            embeddings = await self.get_embedding_model(embedding_model_id)
            
            # 获取集合名称
            collection_name = self._get_collection_name(kb_id)
            
            # 创建向量存储
            vector_store = Chroma(
                collection_name=collection_name,
                embedding_function=embeddings,
                persist_directory=str(self.persist_directory),
            )
            
            # 执行相似度搜索
            results = vector_store.similarity_search_with_relevance_scores(
                query=query,
                k=top_k,
            )
            
            # 过滤并格式化结果
            formatted_results = []
            for doc, score in results:
                if score >= score_threshold:
                    formatted_results.append({
                        "content": doc.page_content,
                        "source": doc.metadata.get("doc_id", "unknown"),
                        "score": score,
                        "metadata": doc.metadata,
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"[VectorStoreService] Failed to search: {e}")
            return []
    
    async def delete_document(self, kb_id: str, doc_id: str) -> bool:
        """
        删除文档的所有向量
        
        Args:
            kb_id: 知识库ID
            doc_id: 文档ID
            
        Returns:
            bool: 是否成功删除
        """
        try:
            # 获取集合名称
            collection_name = self._get_collection_name(kb_id)
            
            # 获取集合
            collection = self.client.get_collection(collection_name)
            
            # 删除该文档的所有向量
            collection.delete(
                where={"doc_id": doc_id}
            )
            
            return True
            
        except Exception as e:
            print(f"[VectorStoreService] Failed to delete document vectors: {e}")
            return False
    
    async def delete_knowledge_base(self, kb_id: str) -> bool:
        """
        删除整个知识库的向量集合
        
        Args:
            kb_id: 知识库ID
            
        Returns:
            bool: 是否成功删除
        """
        try:
            # 获取集合名称
            collection_name = self._get_collection_name(kb_id)
            
            # 删除集合
            self.client.delete_collection(collection_name)
            
            return True
            
        except Exception as e:
            print(f"[VectorStoreService] Failed to delete collection: {e}")
            return False
    
    async def get_stats(self, kb_id: str) -> dict:
        """
        获取知识库向量统计信息
        
        Args:
            kb_id: 知识库ID
            
        Returns:
            dict: 统计信息
        """
        try:
            # 获取集合名称
            collection_name = self._get_collection_name(kb_id)
            
            # 获取集合
            collection = self.client.get_collection(collection_name)
            
            return {
                "count": collection.count(),
                "name": collection_name,
            }
            
        except Exception as e:
            print(f"[VectorStoreService] Failed to get stats: {e}")
            return {"count": 0, "name": ""}
