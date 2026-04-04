"""
LangGraph 状态类型定义

定义 Agent 工作流中传递的状态数据结构
"""

from typing import Annotated, Any, Dict, List, Optional, Sequence
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    Agent 工作流状态
    
    在 LangGraph 的各节点之间传递的状态对象
    """
    # 消息历史（使用 add_messages reducer 自动合并）
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # 用户输入（原始问题）
    input: str
    
    # 预设方案ID
    preset_id: str
    
    # 会话ID（用于记忆存储）
    session_id: Optional[str]
    
    # RAG检索结果
    retrieved_context: Optional[str]
    
    # 是否需要检索
    needs_retrieval: bool
    
    # 工具调用结果
    tool_results: Optional[List[Dict[str, Any]]]
    
    # 是否需要调用工具
    needs_tool_call: bool
    
    # 当前步骤计数（防止无限循环）
    step_count: int
    
    # 最大步骤数限制
    max_steps: int
    
    # 配置覆盖参数
    overrides: Optional[Dict[str, Any]]
    
    # 错误信息
    error: Optional[str]


class RAGState(TypedDict):
    """
    RAG 检索专用状态
    
    用于 RAG 检索子图的状态
    """
    # 查询文本
    query: str
    
    # 知识库ID列表
    knowledge_base_ids: List[str]
    
    # 检索结果
    documents: List[Dict[str, Any]]
    
    # 格式化后的上下文
    context: Optional[str]
    
    # 嵌入模型ID
    embedding_model_id: Optional[str]
    
    # 检索参数
    retrieval_params: Optional[Dict[str, Any]]


class ToolState(TypedDict):
    """
    工具调用专用状态
    
    用于工具调用子图的状态
    """
    # 工具调用请求
    tool_calls: List[Dict[str, Any]]
    
    # 工具执行结果
    tool_outputs: List[Dict[str, Any]]
    
    # 可用工具列表（插件ID）
    available_tools: List[str]
    
    # 权限级别
    permission_level: int


# 状态初始化辅助函数
def create_initial_state(
    input_message: str,
    preset_id: str,
    session_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    overrides: Optional[Dict[str, Any]] = None
) -> AgentState:
    """
    创建初始状态
    
    Args:
        input_message: 用户输入消息
        preset_id: 预设方案ID
        session_id: 会话ID（可选）
        system_prompt: 系统提示词（可选）
        overrides: 覆盖配置（可选）
        
    Returns:
        AgentState: 初始状态对象
    """
    messages = []
    
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    
    messages.append(HumanMessage(content=input_message))
    
    return AgentState(
        messages=messages,
        input=input_message,
        preset_id=preset_id,
        session_id=session_id,
        retrieved_context=None,
        needs_retrieval=False,
        tool_results=None,
        needs_tool_call=False,
        step_count=0,
        max_steps=10,
        overrides=overrides or {},
        error=None
    )


def format_retrieved_context(documents: List[Dict[str, Any]]) -> str:
    """
    格式化检索结果为上下文字符串
    
    Args:
        documents: 检索到的文档列表
        
    Returns:
        str: 格式化后的上下文
    """
    if not documents:
        return ""
    
    context_parts = []
    for i, doc in enumerate(documents, 1):
        content = doc.get("content", "")
        source = doc.get("source", "unknown")
        score = doc.get("score", 0)
        
        context_parts.append(
            f"[{i}] {content}\n（来源：{source}，相关度：{score:.2f}）"
        )
    
    return "\n\n".join(context_parts)
