"""
配置导入导出服务

提供五大资源池和预设方案的 YAML/JSON 导入导出功能
"""

import json
import logging
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    KnowledgeBase,
    MemoryConfig,
    ModelConfig,
    PluginConfig,
    Preset,
    PromptConfig,
)

logger = logging.getLogger(__name__)

EXPORT_VERSION = "1.0"


class ExportType(str, Enum):
    """导出类型"""
    MODEL = "model"
    PROMPT = "prompt"
    PLUGIN = "plugin"
    KNOWLEDGE_BASE = "knowledge_base"
    MEMORY = "memory"
    PRESET = "preset"
    BATCH = "batch"


class ImportConflictAction(str, Enum):
    """导入冲突处理动作"""
    SKIP = "skip"
    OVERWRITE = "overwrite"
    RENAME = "rename"


class ImportResult(BaseModel):
    """导入结果"""
    success: bool
    action: str  # created / updated / skipped / renamed
    original_id: Optional[str] = None
    new_id: Optional[str] = None
    message: str = ""


class ImportReport(BaseModel):
    """导入报告"""
    total: int
    success: int
    failed: int
    skipped: int
    results: List[ImportResult] = []


class ExportService:
    """配置导出服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def export_model(self, model_id: str, include_resources: bool = False) -> Dict[str, Any]:
        """导出模型配置"""
        result = await self.db.execute(
            select(ModelConfig).where(ModelConfig.model_id == model_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"模型配置 '{model_id}' 不存在")

        data = model.to_dict()
        # 移除内部字段
        data.pop("id", None)
        data.pop("created_at", None)
        data.pop("updated_at", None)
        # api_key 不导出
        data.pop("api_key", None)

        export_data = {
            "export_type": ExportType.MODEL.value,
            "export_version": EXPORT_VERSION,
            "export_time": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }

        return export_data

    async def export_prompt(self, prompt_id: str) -> Dict[str, Any]:
        """导出提示词配置"""
        result = await self.db.execute(
            select(PromptConfig).where(PromptConfig.prompt_id == prompt_id)
        )
        prompt = result.scalar_one_or_none()
        if not prompt:
            raise ValueError(f"提示词配置 '{prompt_id}' 不存在")

        data = prompt.to_dict()
        data.pop("id", None)
        data.pop("created_at", None)
        data.pop("updated_at", None)

        return {
            "export_type": ExportType.PROMPT.value,
            "export_version": EXPORT_VERSION,
            "export_time": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }

    async def export_plugin(self, plugin_id: str) -> Dict[str, Any]:
        """导出插件配置"""
        result = await self.db.execute(
            select(PluginConfig).where(PluginConfig.plugin_id == plugin_id)
        )
        plugin = result.scalar_one_or_none()
        if not plugin:
            raise ValueError(f"插件配置 '{plugin_id}' 不存在")

        data = plugin.to_dict()
        data.pop("id", None)
        data.pop("created_at", None)
        data.pop("updated_at", None)

        return {
            "export_type": ExportType.PLUGIN.value,
            "export_version": EXPORT_VERSION,
            "export_time": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }

    async def export_knowledge_base(self, kb_id: str) -> Dict[str, Any]:
        """导出知识库配置（不含向量数据）"""
        result = await self.db.execute(
            select(KnowledgeBase).where(KnowledgeBase.kb_id == kb_id)
        )
        kb = result.scalar_one_or_none()
        if not kb:
            raise ValueError(f"知识库配置 '{kb_id}' 不存在")

        data = kb.to_dict()
        data.pop("id", None)
        data.pop("created_at", None)
        data.pop("updated_at", None)

        return {
            "export_type": ExportType.KNOWLEDGE_BASE.value,
            "export_version": EXPORT_VERSION,
            "export_time": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }

    async def export_memory(self, memory_id: str) -> Dict[str, Any]:
        """导出记忆配置"""
        result = await self.db.execute(
            select(MemoryConfig).where(MemoryConfig.memory_id == memory_id)
        )
        memory = result.scalar_one_or_none()
        if not memory:
            raise ValueError(f"记忆配置 '{memory_id}' 不存在")

        data = memory.to_dict()
        data.pop("id", None)
        data.pop("created_at", None)
        data.pop("updated_at", None)

        return {
            "export_type": ExportType.MEMORY.value,
            "export_version": EXPORT_VERSION,
            "export_time": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }

    async def export_preset(self, preset_id: str, include_resources: bool = False) -> Dict[str, Any]:
        """
        导出预设方案
        
        Args:
            preset_id: 预设方案ID
            include_resources: 是否包含引用的资源（模型/提示词/插件/知识库/记忆）
        """
        result = await self.db.execute(
            select(Preset).where(Preset.preset_id == preset_id)
        )
        preset = result.scalar_one_or_none()
        if not preset:
            raise ValueError(f"预设方案 '{preset_id}' 不存在")

        data = preset.to_dict()
        data.pop("id", None)
        data.pop("created_at", None)
        data.pop("updated_at", None)

        export_data = {
            "export_type": ExportType.PRESET.value,
            "export_version": EXPORT_VERSION,
            "export_time": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }

        # 可选：包含引用的资源
        if include_resources:
            resources = {}
            
            # 导出模型配置
            if preset.selected_model:
                model_result = await self.db.execute(
                    select(ModelConfig).where(ModelConfig.model_name.contains([preset.selected_model]))
                )
                model = model_result.scalar_one_or_none()
                if model:
                    model_data = model.to_dict()
                    model_data.pop("id", None)
                    model_data.pop("created_at", None)
                    model_data.pop("updated_at", None)
                    model_data.pop("api_key", None)
                    resources["models"] = [model_data]

            # 导出提示词
            if preset.selected_prompt:
                prompt_result = await self.db.execute(
                    select(PromptConfig).where(PromptConfig.prompt_id == preset.selected_prompt)
                )
                prompt = prompt_result.scalar_one_or_none()
                if prompt:
                    prompt_data = prompt.to_dict()
                    prompt_data.pop("id", None)
                    prompt_data.pop("created_at", None)
                    prompt_data.pop("updated_at", None)
                    resources["prompts"] = [prompt_data]

            # 导出插件
            if preset.selected_plugins:
                plugins = []
                for plugin_id in preset.selected_plugins:
                    plugin_result = await self.db.execute(
                        select(PluginConfig).where(PluginConfig.plugin_id == plugin_id)
                    )
                    plugin = plugin_result.scalar_one_or_none()
                    if plugin:
                        plugin_data = plugin.to_dict()
                        plugin_data.pop("id", None)
                        plugin_data.pop("created_at", None)
                        plugin_data.pop("updated_at", None)
                        plugins.append(plugin_data)
                if plugins:
                    resources["plugins"] = plugins

            # 导出知识库
            if preset.selected_knowledge_bases:
                kbs = []
                for kb_id in preset.selected_knowledge_bases:
                    kb_result = await self.db.execute(
                        select(KnowledgeBase).where(KnowledgeBase.kb_id == kb_id)
                    )
                    kb = kb_result.scalar_one_or_none()
                    if kb:
                        kb_data = kb.to_dict()
                        kb_data.pop("id", None)
                        kb_data.pop("created_at", None)
                        kb_data.pop("updated_at", None)
                        kbs.append(kb_data)
                if kbs:
                    resources["knowledge_bases"] = kbs

            # 导出记忆
            if preset.selected_memory:
                memory_result = await self.db.execute(
                    select(MemoryConfig).where(MemoryConfig.memory_id == preset.selected_memory)
                )
                memory = memory_result.scalar_one_or_none()
                if memory:
                    memory_data = memory.to_dict()
                    memory_data.pop("id", None)
                    memory_data.pop("created_at", None)
                    memory_data.pop("updated_at", None)
                    resources["memories"] = [memory_data]

            export_data["resources"] = resources

        return export_data

    def to_yaml(self, export_data: Dict[str, Any]) -> str:
        """转换为 YAML 格式"""
        return yaml.dump(export_data, allow_unicode=True, default_flow_style=False, sort_keys=False)

    def to_json(self, export_data: Dict[str, Any], indent: int = 2) -> str:
        """转换为 JSON 格式"""
        return json.dumps(export_data, ensure_ascii=False, indent=indent)


class ImportService:
    """配置导入服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    def parse_content(self, content: str, format: str = "yaml") -> Dict[str, Any]:
        """解析导入内容"""
        try:
            if format == "json":
                return json.loads(content)
            else:
                return yaml.safe_load(content)
        except Exception as e:
            raise ValueError(f"解析失败：{str(e)}")

    async def import_model(self, data: Dict[str, Any], conflict_action: str = ImportConflictAction.RENAME.value) -> ImportResult:
        """导入模型配置"""
        model_id = data.get("model_id")
        if not model_id:
            return ImportResult(success=False, action="failed", message="缺少 model_id")

        # 检查是否存在
        result = await self.db.execute(
            select(ModelConfig).where(ModelConfig.model_id == model_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            if conflict_action == ImportConflictAction.SKIP.value:
                return ImportResult(success=True, action="skipped", original_id=model_id, message="已存在，跳过")
            elif conflict_action == ImportConflictAction.OVERWRITE.value:
                # 更新现有配置
                for key, value in data.items():
                    if key not in ("id", "created_at", "updated_at"):
                        setattr(existing, key, value)
                await self.db.commit()
                return ImportResult(success=True, action="updated", original_id=model_id, message="已更新")
            else:
                # RENAME: 生成新ID
                new_id = f"{model_id}_{uuid.uuid4().hex[:6]}"
                data["model_id"] = new_id

        # 创建新配置
        model = ModelConfig(**{k: v for k, v in data.items() if k not in ("id", "created_at", "updated_at")})
        self.db.add(model)
        await self.db.commit()
        
        return ImportResult(
            success=True, 
            action="created" if not existing else "renamed",
            original_id=model_id,
            new_id=data["model_id"],
            message="导入成功"
        )

    async def import_prompt(self, data: Dict[str, Any], conflict_action: str = ImportConflictAction.RENAME.value) -> ImportResult:
        """导入提示词配置"""
        prompt_id = data.get("prompt_id")
        if not prompt_id:
            return ImportResult(success=False, action="failed", message="缺少 prompt_id")

        result = await self.db.execute(
            select(PromptConfig).where(PromptConfig.prompt_id == prompt_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            if conflict_action == ImportConflictAction.SKIP.value:
                return ImportResult(success=True, action="skipped", original_id=prompt_id, message="已存在，跳过")
            elif conflict_action == ImportConflictAction.OVERWRITE.value:
                for key, value in data.items():
                    if key not in ("id", "created_at", "updated_at"):
                        setattr(existing, key, value)
                await self.db.commit()
                return ImportResult(success=True, action="updated", original_id=prompt_id, message="已更新")
            else:
                new_id = f"{prompt_id}_{uuid.uuid4().hex[:6]}"
                data["prompt_id"] = new_id

        prompt = PromptConfig(**{k: v for k, v in data.items() if k not in ("id", "created_at", "updated_at")})
        self.db.add(prompt)
        await self.db.commit()
        
        return ImportResult(
            success=True,
            action="created" if not existing else "renamed",
            original_id=prompt_id,
            new_id=data.get("prompt_id"),
            message="导入成功"
        )

    async def import_plugin(self, data: Dict[str, Any], conflict_action: str = ImportConflictAction.RENAME.value) -> ImportResult:
        """导入插件配置"""
        plugin_id = data.get("plugin_id")
        if not plugin_id:
            return ImportResult(success=False, action="failed", message="缺少 plugin_id")

        result = await self.db.execute(
            select(PluginConfig).where(PluginConfig.plugin_id == plugin_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            if conflict_action == ImportConflictAction.SKIP.value:
                return ImportResult(success=True, action="skipped", original_id=plugin_id, message="已存在，跳过")
            elif conflict_action == ImportConflictAction.OVERWRITE.value:
                for key, value in data.items():
                    if key not in ("id", "created_at", "updated_at"):
                        setattr(existing, key, value)
                await self.db.commit()
                return ImportResult(success=True, action="updated", original_id=plugin_id, message="已更新")
            else:
                new_id = f"{plugin_id}_{uuid.uuid4().hex[:6]}"
                data["plugin_id"] = new_id

        plugin = PluginConfig(**{k: v for k, v in data.items() if k not in ("id", "created_at", "updated_at")})
        self.db.add(plugin)
        await self.db.commit()
        
        return ImportResult(
            success=True,
            action="created" if not existing else "renamed",
            original_id=plugin_id,
            new_id=data.get("plugin_id"),
            message="导入成功"
        )

    async def import_knowledge_base(self, data: Dict[str, Any], conflict_action: str = ImportConflictAction.RENAME.value) -> ImportResult:
        """导入知识库配置"""
        kb_id = data.get("kb_id")
        if not kb_id:
            return ImportResult(success=False, action="failed", message="缺少 kb_id")

        result = await self.db.execute(
            select(KnowledgeBase).where(KnowledgeBase.kb_id == kb_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            if conflict_action == ImportConflictAction.SKIP.value:
                return ImportResult(success=True, action="skipped", original_id=kb_id, message="已存在，跳过")
            elif conflict_action == ImportConflictAction.OVERWRITE.value:
                for key, value in data.items():
                    if key not in ("id", "created_at", "updated_at"):
                        setattr(existing, key, value)
                await self.db.commit()
                return ImportResult(success=True, action="updated", original_id=kb_id, message="已更新")
            else:
                new_id = f"{kb_id}_{uuid.uuid4().hex[:6]}"
                data["kb_id"] = new_id

        kb = KnowledgeBase(**{k: v for k, v in data.items() if k not in ("id", "created_at", "updated_at")})
        self.db.add(kb)
        await self.db.commit()
        
        return ImportResult(
            success=True,
            action="created" if not existing else "renamed",
            original_id=kb_id,
            new_id=data.get("kb_id"),
            message="导入成功"
        )

    async def import_memory(self, data: Dict[str, Any], conflict_action: str = ImportConflictAction.RENAME.value) -> ImportResult:
        """导入记忆配置"""
        memory_id = data.get("memory_id")
        if not memory_id:
            return ImportResult(success=False, action="failed", message="缺少 memory_id")

        result = await self.db.execute(
            select(MemoryConfig).where(MemoryConfig.memory_id == memory_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            if conflict_action == ImportConflictAction.SKIP.value:
                return ImportResult(success=True, action="skipped", original_id=memory_id, message="已存在，跳过")
            elif conflict_action == ImportConflictAction.OVERWRITE.value:
                for key, value in data.items():
                    if key not in ("id", "created_at", "updated_at"):
                        setattr(existing, key, value)
                await self.db.commit()
                return ImportResult(success=True, action="updated", original_id=memory_id, message="已更新")
            else:
                new_id = f"{memory_id}_{uuid.uuid4().hex[:6]}"
                data["memory_id"] = new_id

        memory = MemoryConfig(**{k: v for k, v in data.items() if k not in ("id", "created_at", "updated_at")})
        self.db.add(memory)
        await self.db.commit()
        
        return ImportResult(
            success=True,
            action="created" if not existing else "renamed",
            original_id=memory_id,
            new_id=data.get("memory_id"),
            message="导入成功"
        )

    async def import_preset(self, data: Dict[str, Any], conflict_action: str = ImportConflictAction.RENAME.value) -> ImportResult:
        """导入预设方案"""
        preset_id = data.get("preset_id")
        if not preset_id:
            return ImportResult(success=False, action="failed", message="缺少 preset_id")

        result = await self.db.execute(
            select(Preset).where(Preset.preset_id == preset_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            if conflict_action == ImportConflictAction.SKIP.value:
                return ImportResult(success=True, action="skipped", original_id=preset_id, message="已存在，跳过")
            elif conflict_action == ImportConflictAction.OVERWRITE.value:
                for key, value in data.items():
                    if key not in ("id", "created_at", "updated_at"):
                        setattr(existing, key, value)
                await self.db.commit()
                return ImportResult(success=True, action="updated", original_id=preset_id, message="已更新")
            else:
                new_id = f"{preset_id}_{uuid.uuid4().hex[:6]}"
                data["preset_id"] = new_id

        preset = Preset(**{k: v for k, v in data.items() if k not in ("id", "created_at", "updated_at")})
        self.db.add(preset)
        await self.db.commit()
        
        return ImportResult(
            success=True,
            action="created" if not existing else "renamed",
            original_id=preset_id,
            new_id=data.get("preset_id"),
            message="导入成功"
        )

    async def import_batch(self, export_data: Dict[str, Any], conflict_action: str = ImportConflictAction.RENAME.value) -> ImportReport:
        """
        批量导入（包含资源的预设方案）
        
        先导入资源，再导入预设方案
        """
        report = ImportReport(total=0, success=0, failed=0, skipped=0, results=[])
        
        resources = export_data.get("resources", {})
        
        # 导入模型
        for model_data in resources.get("models", []):
            report.total += 1
            try:
                result = await self.import_model(model_data, conflict_action)
                report.results.append(result)
                if result.success:
                    if result.action == "skipped":
                        report.skipped += 1
                    else:
                        report.success += 1
                else:
                    report.failed += 1
            except Exception as e:
                report.failed += 1
                report.results.append(ImportResult(success=False, action="failed", message=str(e)))

        # 导入提示词
        for prompt_data in resources.get("prompts", []):
            report.total += 1
            try:
                result = await self.import_prompt(prompt_data, conflict_action)
                report.results.append(result)
                if result.success:
                    if result.action == "skipped":
                        report.skipped += 1
                    else:
                        report.success += 1
                else:
                    report.failed += 1
            except Exception as e:
                report.failed += 1
                report.results.append(ImportResult(success=False, action="failed", message=str(e)))

        # 导入插件
        for plugin_data in resources.get("plugins", []):
            report.total += 1
            try:
                result = await self.import_plugin(plugin_data, conflict_action)
                report.results.append(result)
                if result.success:
                    if result.action == "skipped":
                        report.skipped += 1
                    else:
                        report.success += 1
                else:
                    report.failed += 1
            except Exception as e:
                report.failed += 1
                report.results.append(ImportResult(success=False, action="failed", message=str(e)))

        # 导入知识库
        for kb_data in resources.get("knowledge_bases", []):
            report.total += 1
            try:
                result = await self.import_knowledge_base(kb_data, conflict_action)
                report.results.append(result)
                if result.success:
                    if result.action == "skipped":
                        report.skipped += 1
                    else:
                        report.success += 1
                else:
                    report.failed += 1
            except Exception as e:
                report.failed += 1
                report.results.append(ImportResult(success=False, action="failed", message=str(e)))

        # 导入记忆
        for memory_data in resources.get("memories", []):
            report.total += 1
            try:
                result = await self.import_memory(memory_data, conflict_action)
                report.results.append(result)
                if result.success:
                    if result.action == "skipped":
                        report.skipped += 1
                    else:
                        report.success += 1
                else:
                    report.failed += 1
            except Exception as e:
                report.failed += 1
                report.results.append(ImportResult(success=False, action="failed", message=str(e)))

        # 导入预设方案
        preset_data = export_data.get("data")
        if preset_data:
            report.total += 1
            try:
                result = await self.import_preset(preset_data, conflict_action)
                report.results.append(result)
                if result.success:
                    if result.action == "skipped":
                        report.skipped += 1
                    else:
                        report.success += 1
                else:
                    report.failed += 1
            except Exception as e:
                report.failed += 1
                report.results.append(ImportResult(success=False, action="failed", message=str(e)))

        return report
