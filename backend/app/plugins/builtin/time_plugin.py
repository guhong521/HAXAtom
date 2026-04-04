"""
时间插件

提供当前时间、日期查询功能
"""

from datetime import datetime
from typing import Any, Dict

from app.plugins.base import BasePlugin, PluginMetadata, PluginResult


class TimePlugin(BasePlugin):
    """
    时间查询插件
    
    功能：
    - 获取当前时间
    - 获取当前日期
    - 获取当前日期时间
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="time",
            description="查询当前时间和日期",
            version="1.0.0",
            author="HAXAtom",
            category="tool",
            icon="🕐",
            tags=["time", "date", "utility"]
        )
    
    async def execute(self, params: Dict[str, Any]) -> PluginResult:
        """
        执行时间查询
        
        Args:
            params: 参数
                - format: 返回格式 (time/date/datetime)
                - timezone: 时区 (默认本地时间)
        
        Returns:
            PluginResult: 时间信息
        """
        try:
            format_type = params.get("format", "datetime")
            
            now = datetime.now()
            
            if format_type == "time":
                result = {
                    "time": now.strftime("%H:%M:%S"),
                    "hour": now.hour,
                    "minute": now.minute,
                    "second": now.second
                }
                message = f"当前时间: {result['time']}"
                
            elif format_type == "date":
                result = {
                    "date": now.strftime("%Y-%m-%d"),
                    "year": now.year,
                    "month": now.month,
                    "day": now.day,
                    "weekday": now.strftime("%A")
                }
                message = f"当前日期: {result['date']} {result['weekday']}"
                
            else:  # datetime
                result = {
                    "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "date": now.strftime("%Y-%m-%d"),
                    "time": now.strftime("%H:%M:%S"),
                    "timestamp": int(now.timestamp())
                }
                message = f"当前时间: {result['datetime']}"
            
            return PluginResult.ok(data=result, message=message)
            
        except Exception as e:
            return PluginResult.error(
                error=str(e),
                message="获取时间信息失败"
            )
    
    def validate_params(self, params: Dict[str, Any]) -> tuple[bool, str]:
        """验证参数"""
        valid_formats = ["time", "date", "datetime"]
        format_type = params.get("format", "datetime")
        
        if format_type not in valid_formats:
            return False, f"无效的format参数，可选值: {', '.join(valid_formats)}"
        
        return True, None
