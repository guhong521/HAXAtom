"""
LangSmith 追踪集成模块

提供全链路追踪、性能监控、调用链路分析功能
"""

import os
from typing import Any, Dict, Optional
from contextlib import contextmanager

from langsmith import Client


class LangSmithTracer:
    """
    LangSmith 追踪管理器
    
    功能：
    1. 自动检测 LangSmith 配置
    2. 提供追踪回调
    3. 记录自定义指标
    4. 管理追踪会话
    """
    
    def __init__(self):
        self.enabled = os.environ.get("LANGCHAIN_TRACING_V2") == "true"
        self.project = os.environ.get("LANGCHAIN_PROJECT", "haxatom")
        self.api_key = os.environ.get("LANGCHAIN_API_KEY")
        self.endpoint = os.environ.get("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
        
        self._client: Optional[Client] = None
        
        if self.enabled and self.api_key:
            try:
                self._client = Client(
                    api_key=self.api_key,
                    api_url=self.endpoint
                )
                print(f"[LangSmith] Tracer initialized for project: {self.project}")
            except Exception as e:
                print(f"[LangSmith] Failed to initialize: {e}")
                self.enabled = False
    
    def is_enabled(self) -> bool:
        """检查追踪是否启用"""
        return self.enabled and self._client is not None
    
    def get_tracer(self):
        """获取 LangChain 追踪回调"""
        # LangSmith 追踪通过环境变量自动启用
        # 不需要手动创建 LangChainTracer
        return None
    
    def create_run_metadata(self, **kwargs) -> Dict[str, Any]:
        """
        创建运行元数据
        
        Args:
            **kwargs: 自定义元数据字段
            
        Returns:
            Dict[str, Any]: 元数据字典
        """
        metadata = {
            "project": self.project,
            **kwargs
        }
        return metadata
    
    @contextmanager
    def trace_run(self, name: str, run_type: str = "chain", **metadata):
        """
        上下文管理器用于追踪代码块
        
        Args:
            name: 运行名称
            run_type: 运行类型 (chain, llm, tool, etc.)
            **metadata: 元数据
            
        Example:
            with tracer.trace_run("my_operation", preset_id="test"):
                result = do_something()
        """
        if not self.is_enabled():
            yield None
            return
        
        try:
            run = self._client.create_run(
                name=name,
                run_type=run_type,
                inputs=metadata.get("inputs", {}),
                extra=metadata
            )
            yield run
        except Exception as e:
            print(f"[LangSmith] Trace error: {e}")
            yield None
    
    def log_feedback(self, run_id: str, key: str, score: float, comment: Optional[str] = None):
        """
        记录用户反馈
        
        Args:
            run_id: 运行ID
            key: 反馈键名
            score: 分数 (0-1)
            comment: 可选评论
        """
        if not self.is_enabled():
            return
        
        try:
            self._client.create_feedback(
                run_id=run_id,
                key=key,
                score=score,
                comment=comment
            )
        except Exception as e:
            print(f"[LangSmith] Feedback error: {e}")


# 全局追踪器实例
_tracer_instance: Optional[LangSmithTracer] = None


def get_tracer() -> LangSmithTracer:
    """获取全局追踪器实例"""
    global _tracer_instance
    if _tracer_instance is None:
        _tracer_instance = LangSmithTracer()
    return _tracer_instance
