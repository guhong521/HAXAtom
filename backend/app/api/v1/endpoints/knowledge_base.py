"""
知识库管理 API

提供知识库的完整管理功能：
- 知识库 CRUD
- 文档上传和管理
- 文档处理和向量化
- 知识库检索
"""

from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.knowledge_base import (
    DocumentList,
    DocumentResponse,
    KnowledgeBaseCreate,
    KnowledgeBaseList,
    KnowledgeBaseResponse,
    KnowledgeBaseUpdate,
    SearchRequest,
    SearchResponse,
    SearchResult,
)
from app.services.knowledge_base_service import KnowledgeBaseService

router = APIRouter()


# ==================== 知识库管理 ====================

@router.post("", response_model=KnowledgeBaseResponse, status_code=status.HTTP_201_CREATED)
async def create_knowledge_base(
    data: KnowledgeBaseCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建知识库
    
    Args:
        data: 知识库创建数据
        
    Returns:
        KnowledgeBaseResponse: 创建的知识库信息
    """
    service = KnowledgeBaseService(db)
    kb = await service.create_knowledge_base(data)
    return kb


@router.get("", response_model=List[KnowledgeBaseList])
async def list_knowledge_bases(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    获取知识库列表
    
    Args:
        skip: 跳过数量
        limit: 返回数量限制
        
    Returns:
        List[KnowledgeBaseList]: 知识库列表
    """
    service = KnowledgeBaseService(db)
    kbs = await service.list_knowledge_bases(skip=skip, limit=limit)
    return kbs


@router.get("/{kb_id}", response_model=KnowledgeBaseResponse)
async def get_knowledge_base(
    kb_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    获取知识库详情
    
    Args:
        kb_id: 知识库ID
        
    Returns:
        KnowledgeBaseResponse: 知识库详情
    """
    service = KnowledgeBaseService(db)
    kb = await service.get_knowledge_base(kb_id)
    
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base '{kb_id}' not found"
        )
    
    return kb


@router.patch("/{kb_id}", response_model=KnowledgeBaseResponse)
async def update_knowledge_base(
    kb_id: str,
    data: KnowledgeBaseUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新知识库
    
    Args:
        kb_id: 知识库ID
        data: 更新数据
        
    Returns:
        KnowledgeBaseResponse: 更新后的知识库信息
    """
    service = KnowledgeBaseService(db)
    kb = await service.update_knowledge_base(kb_id, data)
    
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base '{kb_id}' not found"
        )
    
    return kb


@router.delete("/{kb_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_knowledge_base(
    kb_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    删除知识库
    
    Args:
        kb_id: 知识库ID
    """
    service = KnowledgeBaseService(db)
    success = await service.delete_knowledge_base(kb_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base '{kb_id}' not found"
        )
    
    # 同时删除向量集合
    from app.services.vector_store_service import VectorStoreService
    vector_service = VectorStoreService(db)
    await vector_service.delete_knowledge_base(kb_id)


# ==================== 文档管理 ====================

@router.post("/{kb_id}/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    kb_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    上传文档到知识库
    
    Args:
        kb_id: 知识库ID
        file: 上传的文件
        
    Returns:
        DocumentResponse: 创建的文档信息
    """
    service = KnowledgeBaseService(db)
    
    # 检查知识库是否存在
    kb = await service.get_knowledge_base(kb_id)
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base '{kb_id}' not found"
        )
    
    # 读取文件内容
    content = await file.read()
    
    # 获取文件类型
    filename = file.filename or "unknown"
    file_type = filename.split(".")[-1].lower() if "." in filename else "txt"
    
    # 上传文档
    try:
        doc = await service.upload_document(
            kb_id=kb_id,
            filename=filename,
            content=content,
            file_type=file_type
        )
        return doc
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{kb_id}/documents", response_model=List[DocumentList])
async def list_documents(
    kb_id: str,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    获取知识库的文档列表
    
    Args:
        kb_id: 知识库ID
        skip: 跳过数量
        limit: 返回数量限制
        
    Returns:
        List[DocumentList]: 文档列表
    """
    service = KnowledgeBaseService(db)
    
    # 检查知识库是否存在
    kb = await service.get_knowledge_base(kb_id)
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base '{kb_id}' not found"
        )
    
    docs = await service.list_documents(kb_id, skip=skip, limit=limit)
    return docs


@router.get("/{kb_id}/documents/{doc_id}", response_model=DocumentResponse)
async def get_document(
    kb_id: str,
    doc_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    获取文档详情
    
    Args:
        kb_id: 知识库ID
        doc_id: 文档ID
        
    Returns:
        DocumentResponse: 文档详情
    """
    service = KnowledgeBaseService(db)
    doc = await service.get_document(doc_id)
    
    if not doc or doc.kb_id != kb_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{doc_id}' not found in knowledge base '{kb_id}'"
        )
    
    return doc


@router.post("/{kb_id}/documents/{doc_id}/process", response_model=DocumentResponse)
async def process_document(
    kb_id: str,
    doc_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    处理文档（分块和向量化）
    
    Args:
        kb_id: 知识库ID
        doc_id: 文档ID
        
    Returns:
        DocumentResponse: 处理后的文档信息
    """
    service = KnowledgeBaseService(db)
    
    # 检查文档是否存在
    doc = await service.get_document(doc_id)
    if not doc or doc.kb_id != kb_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{doc_id}' not found in knowledge base '{kb_id}'"
        )
    
    # 处理文档
    success = await service.process_document(doc_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process document"
        )
    
    # 重新获取文档信息
    doc = await service.get_document(doc_id)
    return doc


@router.delete("/{kb_id}/documents/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    kb_id: str,
    doc_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    删除文档
    
    Args:
        kb_id: 知识库ID
        doc_id: 文档ID
    """
    service = KnowledgeBaseService(db)
    
    # 检查文档是否存在
    doc = await service.get_document(doc_id)
    if not doc or doc.kb_id != kb_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{doc_id}' not found in knowledge base '{kb_id}'"
        )
    
    # 删除向量
    from app.services.vector_store_service import VectorStoreService
    vector_service = VectorStoreService(db)
    await vector_service.delete_document(kb_id, doc_id)
    
    # 删除文档
    success = await service.delete_document(doc_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete document"
        )


# ==================== 知识库检索 ====================

@router.post("/{kb_id}/search", response_model=SearchResponse)
async def search_knowledge_base(
    kb_id: str,
    request: SearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    在知识库中检索
    
    Args:
        kb_id: 知识库ID
        request: 检索请求
        
    Returns:
        SearchResponse: 检索结果
    """
    service = KnowledgeBaseService(db)
    
    # 检查知识库是否存在
    kb = await service.get_knowledge_base(kb_id)
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base '{kb_id}' not found"
        )
    
    # 执行检索
    try:
        results = await service.search(
            kb_id=kb_id,
            query=request.query,
            top_k=request.top_k,
            score_threshold=request.score_threshold
        )
        
        # 格式化结果
        search_results = [
            SearchResult(
                content=r["content"],
                source=r["source"],
                score=r["score"],
                metadata=r.get("metadata", {})
            )
            for r in results
        ]
        
        return SearchResponse(
            query=request.query,
            results=search_results,
            total=len(search_results)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )
