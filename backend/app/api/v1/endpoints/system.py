"""
系统信息 API

提供系统监控、资源使用情况等接口
"""

import psutil
import platform
import sys
from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter()

# 系统启动时间
START_TIME = datetime.now()


@router.get("/info")
async def get_system_info() -> Dict[str, Any]:
    """
    获取系统信息
    
    返回：
    - 平台信息
    - Python 版本
    - CPU 信息
    - 内存信息
    - 磁盘信息
    - 运行时长
    """
    try:
        # CPU 信息
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count(logical=True)
        
        # 获取 CPU 型号（不同平台方式不同）
        try:
            if platform.system() == "Windows":
                import winreg
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
                    cpu_model = winreg.QueryValueEx(key, "ProcessorNameString")[0]
            elif platform.system() == "Darwin":
                import subprocess
                result = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True)
                cpu_model = result.stdout.strip()
            else:
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if line.startswith("model name"):
                            cpu_model = line.split(":")[1].strip()
                            break
                    else:
                        cpu_model = "Unknown"
        except Exception:
            cpu_model = "Unknown"
        
        # 内存信息
        memory = psutil.virtual_memory()
        
        # 磁盘信息
        disk = psutil.disk_usage("/")
        
        # 运行时长
        uptime = (datetime.now() - START_TIME).total_seconds()
        
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "cpu_model": cpu_model,
            "cpu_count": cpu_count,
            "cpu_percent": cpu_percent,
            "memory_total": memory.total,
            "memory_available": memory.available,
            "memory_used": memory.used,
            "memory_percent": memory.percent,
            "disk_total": disk.total,
            "disk_used": disk.used,
            "disk_percent": disk.percent,
            "uptime": int(uptime),
            "haxatom_version": "1.0.0",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取系统信息失败：{str(e)}")


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    健康检查接口
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": int((datetime.now() - START_TIME).total_seconds()),
    }
