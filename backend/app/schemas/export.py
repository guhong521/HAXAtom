"""
导入导出 Schema

定义配置导入导出相关的 Pydantic 模型
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ImportRequest(BaseModel):
    """导入请求"""
    content: str = Field(..., description="YAML/JSON 内容")
    format: str = Field(default="yaml", description="格式：yaml 或 json")
    conflict_action: str = Field(
        default="rename",
        description="冲突处理：skip（跳过）/ overwrite（覆盖）/ rename（重命名）"
    )


class ImportResult(BaseModel):
    """单条导入结果"""
    success: bool
    action: str  # created / updated / skipped / renamed / failed
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


class ExportResponse(BaseModel):
    """导出响应"""
    content: str = Field(..., description="导出的 YAML/JSON 内容")
    filename: str = Field(..., description="建议的文件名")
    export_type: str = Field(..., description="导出类型")


class BatchImportRequest(ImportRequest):
    """批量导入请求（包含资源的预设方案）"""
    pass
