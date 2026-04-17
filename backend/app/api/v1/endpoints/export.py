"""
配置导入导出 API

提供五大资源池和预设方案的 YAML/JSON 导入导出接口
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas import (
    BatchImportRequest,
    ExportResponse,
    ImportReport,
    ImportRequest,
    ImportResult,
    ResponseBase,
)
from app.services.export_service import ExportService, ImportService

logger = logging.getLogger(__name__)

router = APIRouter()


# ==================== 模型配置导入导出 ====================

@router.get("/models/{model_id}/export", response_model=ResponseBase[ExportResponse])
async def export_model(
    model_id: str,
    format: str = Query(default="yaml", description="导出格式：yaml 或 json"),
    include_resources: bool = Query(default=False, description="是否包含关联资源"),
    db: AsyncSession = Depends(get_db)
):
    """导出模型配置"""
    service = ExportService(db)
    try:
        export_data = await service.export_model(model_id, include_resources)
        content = service.to_yaml(export_data) if format == "yaml" else service.to_json(export_data)
        filename = f"model_{model_id}.{format}"
        
        return ResponseBase(data=ExportResponse(
            content=content,
            filename=filename,
            export_type="model"
        ))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/models/import", response_model=ResponseBase[ImportResult])
async def import_model(
    request: ImportRequest,
    db: AsyncSession = Depends(get_db)
):
    """导入模型配置"""
    service = ImportService(db)
    try:
        data = service.parse_content(request.content, request.format)
        export_data = data.get("data", data)
        result = await service.import_model(export_data, request.conflict_action)
        return ResponseBase(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== 提示词配置导入导出 ====================

@router.get("/prompts/{prompt_id}/export", response_model=ResponseBase[ExportResponse])
async def export_prompt(
    prompt_id: str,
    format: str = Query(default="yaml", description="导出格式：yaml 或 json"),
    db: AsyncSession = Depends(get_db)
):
    """导出提示词配置"""
    service = ExportService(db)
    try:
        export_data = await service.export_prompt(prompt_id)
        content = service.to_yaml(export_data) if format == "yaml" else service.to_json(export_data)
        filename = f"prompt_{prompt_id}.{format}"
        
        return ResponseBase(data=ExportResponse(
            content=content,
            filename=filename,
            export_type="prompt"
        ))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/prompts/import", response_model=ResponseBase[ImportResult])
async def import_prompt(
    request: ImportRequest,
    db: AsyncSession = Depends(get_db)
):
    """导入提示词配置"""
    service = ImportService(db)
    try:
        data = service.parse_content(request.content, request.format)
        export_data = data.get("data", data)
        result = await service.import_prompt(export_data, request.conflict_action)
        return ResponseBase(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== 插件配置导入导出 ====================

@router.get("/plugins/{plugin_id}/export", response_model=ResponseBase[ExportResponse])
async def export_plugin(
    plugin_id: str,
    format: str = Query(default="yaml", description="导出格式：yaml 或 json"),
    db: AsyncSession = Depends(get_db)
):
    """导出插件配置"""
    service = ExportService(db)
    try:
        export_data = await service.export_plugin(plugin_id)
        content = service.to_yaml(export_data) if format == "yaml" else service.to_json(export_data)
        filename = f"plugin_{plugin_id}.{format}"
        
        return ResponseBase(data=ExportResponse(
            content=content,
            filename=filename,
            export_type="plugin"
        ))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/plugins/import", response_model=ResponseBase[ImportResult])
async def import_plugin(
    request: ImportRequest,
    db: AsyncSession = Depends(get_db)
):
    """导入插件配置"""
    service = ImportService(db)
    try:
        data = service.parse_content(request.content, request.format)
        export_data = data.get("data", data)
        result = await service.import_plugin(export_data, request.conflict_action)
        return ResponseBase(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== 知识库配置导入导出 ====================

@router.get("/knowledge-bases/{kb_id}/export", response_model=ResponseBase[ExportResponse])
async def export_knowledge_base(
    kb_id: str,
    format: str = Query(default="yaml", description="导出格式：yaml 或 json"),
    db: AsyncSession = Depends(get_db)
):
    """导出知识库配置"""
    service = ExportService(db)
    try:
        export_data = await service.export_knowledge_base(kb_id)
        content = service.to_yaml(export_data) if format == "yaml" else service.to_json(export_data)
        filename = f"kb_{kb_id}.{format}"
        
        return ResponseBase(data=ExportResponse(
            content=content,
            filename=filename,
            export_type="knowledge_base"
        ))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/knowledge-bases/import", response_model=ResponseBase[ImportResult])
async def import_knowledge_base(
    request: ImportRequest,
    db: AsyncSession = Depends(get_db)
):
    """导入知识库配置"""
    service = ImportService(db)
    try:
        data = service.parse_content(request.content, request.format)
        export_data = data.get("data", data)
        result = await service.import_knowledge_base(export_data, request.conflict_action)
        return ResponseBase(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== 记忆配置导入导出 ====================

@router.get("/memories/{memory_id}/export", response_model=ResponseBase[ExportResponse])
async def export_memory(
    memory_id: str,
    format: str = Query(default="yaml", description="导出格式：yaml 或 json"),
    db: AsyncSession = Depends(get_db)
):
    """导出记忆配置"""
    service = ExportService(db)
    try:
        export_data = await service.export_memory(memory_id)
        content = service.to_yaml(export_data) if format == "yaml" else service.to_json(export_data)
        filename = f"memory_{memory_id}.{format}"
        
        return ResponseBase(data=ExportResponse(
            content=content,
            filename=filename,
            export_type="memory"
        ))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/memories/import", response_model=ResponseBase[ImportResult])
async def import_memory(
    request: ImportRequest,
    db: AsyncSession = Depends(get_db)
):
    """导入记忆配置"""
    service = ImportService(db)
    try:
        data = service.parse_content(request.content, request.format)
        export_data = data.get("data", data)
        result = await service.import_memory(export_data, request.conflict_action)
        return ResponseBase(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== 预设方案导入导出 ====================

@router.get("/presets/{preset_id}/export", response_model=ResponseBase[ExportResponse])
async def export_preset(
    preset_id: str,
    format: str = Query(default="yaml", description="导出格式：yaml 或 json"),
    include_resources: bool = Query(default=True, description="是否包含引用的资源（模型/提示词/插件/知识库/记忆）"),
    db: AsyncSession = Depends(get_db)
):
    """
    导出预设方案
    
    默认包含引用的所有资源配置，方便一键分享完整配置
    """
    service = ExportService(db)
    try:
        export_data = await service.export_preset(preset_id, include_resources)
        content = service.to_yaml(export_data) if format == "yaml" else service.to_json(export_data)
        filename = f"preset_{preset_id}.{format}"
        
        return ResponseBase(data=ExportResponse(
            content=content,
            filename=filename,
            export_type="preset"
        ))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/presets/import", response_model=ResponseBase[ImportReport])
async def import_preset(
    request: BatchImportRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    导入预设方案（支持批量导入包含的资源）
    
    会自动导入预设引用的模型、提示词、插件、知识库、记忆配置
    """
    service = ImportService(db)
    try:
        export_data = service.parse_content(request.content, request.format)
        report = await service.import_batch(export_data, request.conflict_action)
        return ResponseBase(data=report)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
