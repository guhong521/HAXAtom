"""
记忆配置 API

提供记忆配置的CRUD接口
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.memory_config import (
    MemoryConfigCreate,
    MemoryConfigList,
    MemoryConfigResponse,
    MemoryConfigUpdate,
)
from app.services.memory_service import MemoryService

router = APIRouter()


@router.post("", response_model=MemoryConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_memory_config(
    data: MemoryConfigCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建记忆配置
    
    Args:
        data: 记忆配置创建数据
        
    Returns:
        MemoryConfigResponse: 创建的记忆配置信息
    """
    service = MemoryService(db)
    config = await service.create_memory_config(data)
    return config


@router.get("", response_model=List[MemoryConfigList])
async def list_memory_configs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    获取记忆配置列表
    
    Args:
        skip: 跳过数量
        limit: 返回数量限制
        
    Returns:
        List[MemoryConfigList]: 记忆配置列表
    """
    service = MemoryService(db)
    configs = await service.list_memory_configs(skip=skip, limit=limit)
    return configs


@router.get("/{memory_id}", response_model=MemoryConfigResponse)
async def get_memory_config(
    memory_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    获取记忆配置详情
    
    Args:
        memory_id: 记忆配置ID
        
    Returns:
        MemoryConfigResponse: 记忆配置详情
    """
    service = MemoryService(db)
    config = await service.get_memory_config(memory_id)
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memory config '{memory_id}' not found"
        )
    
    return config


@router.patch("/{memory_id}", response_model=MemoryConfigResponse)
async def update_memory_config(
    memory_id: str,
    data: MemoryConfigUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新记忆配置
    
    Args:
        memory_id: 记忆配置ID
        data: 更新数据
        
    Returns:
        MemoryConfigResponse: 更新后的记忆配置信息
    """
    service = MemoryService(db)
    config = await service.update_memory_config(memory_id, data)
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memory config '{memory_id}' not found"
        )
    
    return config


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory_config(
    memory_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    删除记忆配置
    
    Args:
        memory_id: 记忆配置ID
    """
    service = MemoryService(db)
    success = await service.delete_memory_config(memory_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memory config '{memory_id}' not found"
        )
