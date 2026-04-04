"""
搜索插件（模拟）

提供搜索功能（实际项目中可接入真实搜索API）
"""

from typing import Any, Dict, List

from app.plugins.base import BasePlugin, PluginMetadata, PluginResult


class SearchPlugin(BasePlugin):
    """
    搜索插件
    
    功能：
    - 模拟搜索（返回预设结果）
    - 实际项目中可接入百度/Google/Bing API
    
    配置项：
    - api_key: 搜索API密钥
    - search_engine: 搜索引擎 (baidu/google/bing)
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="search",
            description="搜索网络信息",
            version="1.0.0",
            author="HAXAtom",
            category="search",
            icon="🔍",
            tags=["search", "web", "information"],
            config_schema={
                "type": "object",
                "properties": {
                    "api_key": {"type": "string", "description": "搜索API密钥"},
                    "search_engine": {
                        "type": "string",
                        "enum": ["baidu", "google", "bing"],
                        "default": "baidu"
                    }
                }
            }
        )
    
    async def execute(self, params: Dict[str, Any]) -> PluginResult:
        """
        执行搜索
        
        Args:
            params: 参数
                - query: 搜索关键词
                - limit: 返回结果数量（默认5）
        
        Returns:
            PluginResult: 搜索结果
        """
        try:
            query = params.get("query", "")
            limit = params.get("limit", 5)
            
            if not query:
                return PluginResult.error(
                    error="Empty query",
                    message="请输入搜索关键词"
                )
            
            # 模拟搜索结果（实际项目中接入真实API）
            results = self._mock_search(query, limit)
            
            return PluginResult.ok(
                data={
                    "query": query,
                    "results_count": len(results),
                    "results": results
                },
                message=f"搜索 '{query}' 找到 {len(results)} 条结果"
            )
            
        except Exception as e:
            return PluginResult.error(
                error=str(e),
                message=f"搜索失败: {str(e)}"
            )
    
    def _mock_search(self, query: str, limit: int) -> List[Dict[str, str]]:
        """
        模拟搜索结果
        
        实际项目中替换为真实搜索API调用
        
        Args:
            query: 搜索关键词
            limit: 结果数量
            
        Returns:
            List[Dict]: 搜索结果列表
        """
        # 模拟数据
        mock_results = [
            {
                "title": f"关于 '{query}' 的相关信息",
                "url": f"https://example.com/search?q={query}&id=1",
                "snippet": f"这是关于{query}的第一条搜索结果摘要..."
            },
            {
                "title": f"{query} - 百度百科",
                "url": f"https://baike.baidu.com/item/{query}",
                "snippet": f"{query}的详细定义和介绍..."
            },
            {
                "title": f"{query} 的最新动态",
                "url": f"https://news.example.com/{query}",
                "snippet": f"{query}相关的新闻和动态更新..."
            },
            {
                "title": f"如何学习 {query}",
                "url": f"https://tutorial.example.com/{query}",
                "snippet": f"{query}的学习资源和教程..."
            },
            {
                "title": f"{query} 相关讨论",
                "url": f"https://forum.example.com/topic/{query}",
                "snippet": f"用户关于{query}的讨论和问答..."
            }
        ]
        
        return mock_results[:limit]
    
    def validate_params(self, params: Dict[str, Any]) -> tuple[bool, str]:
        """验证参数"""
        query = params.get("query", "")
        
        if not query:
            return False, "query参数不能为空"
        
        if len(query) > 200:
            return False, "搜索关键词过长（最大200字符）"
        
        return True, None
