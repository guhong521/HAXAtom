"""
HAXAtom 全局配置管理

使用 Pydantic Settings 管理环境变量和配置
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    应用配置类
    
    自动从环境变量加载配置，支持 .env 文件
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # 应用配置
    app_name: str = "HAXAtom"
    app_version: str = "0.1.0"
    debug: bool = False  # 默认关闭debug，减少日志输出
    secret_key: str = "change-this-in-production"
    
    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000
    
    # 数据库配置
    database_url: str = "sqlite+aiosqlite:///data/db/haxatom.db"
    
    # 向量存储配置
    chroma_persist_dir: str = "data/chroma"
    
    # LangSmith配置
    langsmith_tracing: bool = False
    langsmith_api_key: Optional[str] = None
    langsmith_project: str = "haxatom"
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    
    # 默认模型配置
    default_model_provider: Optional[str] = None
    default_model_api_key: Optional[str] = None
    default_model_api_base: Optional[str] = None
    
    # 安全配置
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "data/logs/haxatom.log"
    
    @property
    def langsmith_config(self) -> dict:
        """LangSmith配置字典"""
        return {
            "tracing": self.langsmith_tracing,
            "api_key": self.langsmith_api_key,
            "project": self.langsmith_project,
            "endpoint": self.langsmith_endpoint,
        }


@lru_cache()
def get_settings() -> Settings:
    """
    获取配置单例
    
    使用 lru_cache 确保配置只加载一次
    """
    return Settings()


# 全局配置实例
settings = get_settings()
