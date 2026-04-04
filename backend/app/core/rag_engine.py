"""
RAG 检索引擎

基于 LCEL 实现的检索增强生成引擎
支持多知识库检索、重排序、上下文注入
"""

from typing import Any, Dict, List, Optional

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_core.vectorstores import VectorStoreRetriever
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.state_types import RAGState, format_retrieved_context
from app.models import KnowledgeBase
from app.services.vector_store_service import VectorStoreService


class RAGEngine:
    """
    RAG 检索引擎
    
    职责：
    1. 多知识库并行检索
    2. 结果重排序（可选）
    3. 上下文格式化
    4. LCEL 链组装
    """
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.vector_service = VectorStoreService(db_session)
    
    async def _get_kb_embedding_model(self, kb_id: str) -> Optional[str]:
        """获取知识库的嵌入模型ID"""
        result = await self.db.execute(
            select(KnowledgeBase).where(KnowledgeBase.kb_id == kb_id)
        )
        kb = result.scalar_one_or_none()
        if kb:
            return kb.embedding_model
        return None
    
    async def retrieve(
        self,
        query: str,
        knowledge_base_ids: List[str],
        top_k: int = 5,
        score_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        从多个知识库检索相关文档
        
        Args:
            query: 查询文本
            knowledge_base_ids: 知识库ID列表
            top_k: 每个知识库返回的最大结果数
            score_threshold: 相似度阈值
            
        Returns:
            List[Dict]: 检索结果列表，按相似度排序
        """
        all_results = []
        
        for kb_id in knowledge_base_ids:
            try:
                # 获取知识库的嵌入模型
                embedding_model_id = await self._get_kb_embedding_model(kb_id)
                if not embedding_model_id:
                    print(f"[RAGEngine] 知识库 {kb_id} 未找到或未配置嵌入模型")
                    continue
                
                results = await self.vector_service.search(
                    kb_id=kb_id,
                    query=query,
                    embedding_model_id=embedding_model_id,
                    top_k=top_k,
                    score_threshold=score_threshold
                )
                all_results.extend(results)
            except Exception as e:
                print(f"[RAGEngine] 知识库 {kb_id} 检索失败: {e}")
        
        # 按相似度排序
        all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        # 返回前 top_k 个结果
        return all_results[:top_k]
    
    def create_retrieval_chain(self) -> RunnableLambda:
        """
        创建 LCEL 检索链
        
        Returns:
            RunnableLambda: 可运行的检索链
        """
        async def _retrieve(state: RAGState) -> RAGState:
            """检索节点函数"""
            documents = await self.retrieve(
                query=state["query"],
                knowledge_base_ids=state["knowledge_base_ids"],
                top_k=state.get("retrieval_params", {}).get("top_k", 5),
                score_threshold=state.get("retrieval_params", {}).get("score_threshold", 0.5)
            )
            
            # 格式化上下文
            context = format_retrieved_context(documents)
            
            return RAGState(
                query=state["query"],
                knowledge_base_ids=state["knowledge_base_ids"],
                documents=documents,
                context=context,
                embedding_model_id=state.get("embedding_model_id"),
                retrieval_params=state.get("retrieval_params")
            )
        
        return RunnableLambda(_retrieve)
    
    async def build_rag_chain(
        self,
        knowledge_base_ids: List[str],
        embedding_model_id: Optional[str] = None,
        retrieval_params: Optional[Dict[str, Any]] = None
    ) -> RunnableLambda:
        """
        构建完整的 RAG 检索链
        
        Args:
            knowledge_base_ids: 知识库ID列表
            embedding_model_id: 嵌入模型ID（可选）
            retrieval_params: 检索参数（可选）
            
        Returns:
            RunnableLambda: RAG检索链
        """
        default_params = {
            "top_k": 5,
            "score_threshold": 0.5
        }
        if retrieval_params:
            default_params.update(retrieval_params)
        
        async def _rag_retrieve(query: str) -> Dict[str, Any]:
            """执行RAG检索"""
            state = RAGState(
                query=query,
                knowledge_base_ids=knowledge_base_ids,
                documents=[],
                context=None,
                embedding_model_id=embedding_model_id,
                retrieval_params=default_params
            )
            
            # 执行检索
            documents = await self.retrieve(
                query=query,
                knowledge_base_ids=knowledge_base_ids,
                top_k=default_params["top_k"],
                score_threshold=default_params["score_threshold"]
            )
            
            # 格式化上下文
            context = format_retrieved_context(documents)
            
            return {
                "query": query,
                "documents": documents,
                "context": context
            }
        
        return RunnableLambda(_rag_retrieve)
    
    async def create_contextualize_chain(
        self,
        model: Any,
        system_prompt: Optional[str] = None
    ) -> RunnableLambda:
        """
        创建查询重写链（用于多轮对话）
        
        将对话历史重写为独立的查询语句
        
        Args:
            model: 语言模型实例
            system_prompt: 系统提示词（可选）
            
        Returns:
            RunnableLambda: 查询重写链
        """
        from langchain_core.prompts import ChatPromptTemplate
        
        default_prompt = """根据聊天历史和最新的用户问题，将用户问题改写为一个独立的查询语句。
这个查询语句应该包含必要的上下文信息，使其在没有历史对话的情况下也能被理解。

注意：不要回答用户的问题，只需要改写查询语句。"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt or default_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}")
        ])
        
        # LCEL 链: prompt | model
        chain = prompt | model
        
        async def _contextualize(state: Dict[str, Any]) -> str:
            """重写查询"""
            chat_history = state.get("chat_history", [])
            if not chat_history:
                return state["input"]
            
            result = await chain.ainvoke({
                "chat_history": chat_history,
                "input": state["input"]
            })
            
            return result.content if hasattr(result, "content") else str(result)
        
        return RunnableLambda(_contextualize)


def create_rag_retriever(
    db: AsyncSession,
    knowledge_base_ids: List[str],
    top_k: int = 5,
    score_threshold: float = 0.5
) -> RunnableLambda:
    """
    创建 RAG 检索器（便捷函数）
    
    Args:
        db: 数据库会话
        knowledge_base_ids: 知识库ID列表
        top_k: 返回结果数
        score_threshold: 相似度阈值
        
    Returns:
        RunnableLambda: RAG检索器
    """
    engine = RAGEngine(db)
    
    async def _retrieve(query: str) -> Dict[str, Any]:
        documents = await engine.retrieve(
            query=query,
            knowledge_base_ids=knowledge_base_ids,
            top_k=top_k,
            score_threshold=score_threshold
        )
        
        context = format_retrieved_context(documents)
        
        return {
            "query": query,
            "documents": documents,
            "context": context
        }
    
    return RunnableLambda(_retrieve)
