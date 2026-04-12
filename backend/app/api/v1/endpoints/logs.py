"""
日志管理端点

提供系统日志的查看、过滤和下载功能
"""

from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from pathlib import Path
from typing import Optional, List
import os

from app.config import settings

router = APIRouter()

# 日志文件路径
LOG_DIR = Path(__file__).parent / "../../../../data/logs"
LOG_FILE = LOG_DIR / "haxatom.log"


@router.get("", summary="获取系统日志")
async def get_logs(
    lines: int = Query(default=100, ge=1, le=1000, description="返回最近 N 行日志"),
    level: Optional[str] = Query(default=None, description="过滤日志级别：INFO, WARNING, ERROR, DEBUG"),
    search: Optional[str] = Query(default=None, description="关键词搜索")
):
    """
    获取最近 N 行系统日志
    
    - **lines**: 返回最近 N 行（默认 100，最大 1000）
    - **level**: 可选，过滤特定日志级别（INFO/WARNING/ERROR/DEBUG）
    - **search**: 可选，关键词搜索（不区分大小写）
    
    返回日志列表，每行一个字符串
    """
    if not LOG_FILE.exists():
        return []
    
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            logs = all_lines[-lines:]
        
        # 按级别过滤
        if level:
            level_upper = level.upper()
            logs = [log for log in logs if level_upper in log]
        
        # 关键词搜索
        if search:
            search_lower = search.lower()
            logs = [log for log in logs if search_lower in log.lower()]
        
        return logs
    
    except Exception as e:
        return [f"读取日志文件失败：{str(e)}"]


@router.get("/download", summary="下载日志文件")
async def download_logs():
    """
    下载完整的日志文件
    
    返回 text/plain 类型的文件响应
    """
    if not LOG_FILE.exists():
        return {"error": "日志文件不存在", "detail": "系统尚未生成任何日志"}
    
    try:
        return FileResponse(
            LOG_FILE,
            media_type='text/plain; charset=utf-8',
            filename='haxatom.log',
            headers={
                'Content-Disposition': 'attachment; filename="haxatom.log"'
            }
        )
    except Exception as e:
        return {"error": "下载失败", "detail": str(e)}


@router.get("/stats", summary="获取日志统计信息")
async def get_log_stats():
    """
    获取日志统计信息
    
    返回各日志级别的数量统计
    """
    if not LOG_FILE.exists():
        return {
            "total": 0,
            "info": 0,
            "warning": 0,
            "error": 0,
            "debug": 0,
            "file_exists": False
        }
    
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
        
        stats = {
            "total": len(all_lines),
            "info": sum(1 for line in all_lines if "INFO" in line),
            "warning": sum(1 for line in all_lines if "WARNING" in line),
            "error": sum(1 for line in all_lines if "ERROR" in line),
            "debug": sum(1 for line in all_lines if "DEBUG" in line),
            "file_exists": True,
            "file_size": os.path.getsize(LOG_FILE)
        }
        
        return stats
    
    except Exception as e:
        return {
            "error": str(e),
            "file_exists": False
        }
