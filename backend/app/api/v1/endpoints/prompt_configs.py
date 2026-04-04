"""
提示词配置 API

提供提示词配置的CRUD接口
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import PromptConfig
from app.schemas import (
    PromptConfigCreate,
    PromptConfigInDB,
    PromptConfigList,
    PromptConfigUpdate,
    ResponseBase,
)

router = APIRouter()


@router.get("", response_model=ResponseBase[List[PromptConfigList]])
async def list_prompts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """获取提示词配置列表"""
    result = await db.execute(
        select(PromptConfig).offset(skip).limit(limit)
    )
    prompts = result.scalars().all()
    
    return ResponseBase(data=[
        PromptConfigList(
            prompt_id=p.prompt_id,
            prompt_name=p.prompt_name,
            description=p.description,
            is_active=p.is_active
        ) for p in prompts
    ])


@router.get("/{prompt_id}", response_model=ResponseBase[PromptConfigInDB])
async def get_prompt(
    prompt_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取提示词配置详情"""
    result = await db.execute(
        select(PromptConfig).where(PromptConfig.prompt_id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    return ResponseBase(data=PromptConfigInDB.model_validate(prompt))


@router.post("", response_model=ResponseBase[PromptConfigInDB])
async def create_prompt(
    prompt: PromptConfigCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建提示词配置"""
    # 检查ID是否已存在
    result = await db.execute(
        select(PromptConfig).where(PromptConfig.prompt_id == prompt.prompt_id)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Prompt ID already exists")
    
    db_prompt = PromptConfig(**prompt.model_dump())
    db.add(db_prompt)
    await db.commit()
    await db.refresh(db_prompt)
    
    return ResponseBase(data=PromptConfigInDB.model_validate(db_prompt))


@router.put("/{prompt_id}", response_model=ResponseBase[PromptConfigInDB])
async def update_prompt(
    prompt_id: str,
    prompt_update: PromptConfigUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新提示词配置"""
    result = await db.execute(
        select(PromptConfig).where(PromptConfig.prompt_id == prompt_id)
    )
    db_prompt = result.scalar_one_or_none()
    
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # 更新字段
    update_data = prompt_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_prompt, field, value)
    
    await db.commit()
    await db.refresh(db_prompt)
    
    return ResponseBase(data=PromptConfigInDB.model_validate(db_prompt))


@router.delete("/{prompt_id}")
async def delete_prompt(
    prompt_id: str,
    db: AsyncSession = Depends(get_db)
):
    """删除提示词配置"""
    result = await db.execute(
        select(PromptConfig).where(PromptConfig.prompt_id == prompt_id)
    )
    db_prompt = result.scalar_one_or_none()
    
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    await db.delete(db_prompt)
    await db.commit()
    
    return ResponseBase(message="Prompt deleted successfully")
