"""
模型配置 API

提供模型配置的CRUD接口
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import ModelConfig
from app.schemas import (
    ModelConfigCreate,
    ModelConfigInDB,
    ModelConfigList,
    ModelConfigResponse,
    ModelConfigUpdate,
    ResponseBase,
)

router = APIRouter()


@router.get("", response_model=ResponseBase[List[ModelConfigList]])
async def list_models(
    skip: int = 0,
    limit: int = 100,
    model_type: str = None,
    db: AsyncSession = Depends(get_db)
):
    """获取模型配置列表"""
    query = select(ModelConfig)
    
    if model_type:
        query = query.where(ModelConfig.model_type == model_type)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    models = result.scalars().all()
    
    return ResponseBase(data=[
        ModelConfigList(
            id=m.id,
            model_id=m.model_id,
            model_name=m.model_name,
            model_type=m.model_type,
            provider=m.provider,
            api_base=m.api_base,
            api_key=m.api_key,
            is_active=m.is_active
        ) for m in models
    ])


@router.get("/{model_id}", response_model=ResponseBase[ModelConfigResponse])
async def get_model(
    model_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取模型配置详情"""
    result = await db.execute(
        select(ModelConfig).where(ModelConfig.model_id == model_id)
    )
    model = result.scalar_one_or_none()
    
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return ResponseBase(data=ModelConfigResponse.model_validate(model))


@router.post("", response_model=ResponseBase[ModelConfigInDB])
async def create_model(
    model: ModelConfigCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建模型配置"""
    # 检查ID是否已存在
    result = await db.execute(
        select(ModelConfig).where(ModelConfig.model_id == model.model_id)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Model ID already exists")
    
    db_model = ModelConfig(**model.model_dump())
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    
    return ResponseBase(data=ModelConfigInDB.model_validate(db_model))


@router.put("/{model_id}", response_model=ResponseBase[ModelConfigInDB])
async def update_model(
    model_id: str,
    model_update: ModelConfigUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新模型配置"""
    result = await db.execute(
        select(ModelConfig).where(ModelConfig.model_id == model_id)
    )
    db_model = result.scalar_one_or_none()
    
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # 更新字段
    update_data = model_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_model, field, value)
    
    await db.commit()
    await db.refresh(db_model)
    
    return ResponseBase(data=ModelConfigInDB.model_validate(db_model))


@router.delete("/{model_id}")
async def delete_model(
    model_id: str,
    db: AsyncSession = Depends(get_db)
):
    """删除模型配置"""
    result = await db.execute(
        select(ModelConfig).where(ModelConfig.model_id == model_id)
    )
    db_model = result.scalar_one_or_none()
    
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    await db.delete(db_model)
    await db.commit()
    
    return ResponseBase(message="Model deleted successfully")
