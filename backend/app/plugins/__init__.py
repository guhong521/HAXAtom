"""
插件系统

提供插件框架和内置插件
"""

from app.plugins.base import BasePlugin, PluginMetadata, PluginResult
from app.plugins.loader import PluginLoader
from app.plugins.registry import PluginRegistry, registry

__all__ = [
    "BasePlugin",
    "PluginMetadata",
    "PluginResult",
    "PluginLoader",
    "PluginRegistry",
    "registry",
]
