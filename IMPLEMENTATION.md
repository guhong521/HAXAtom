# HAXAtom 项目详细实现方案

## 目录

1. [项目目录结构](#一项目目录结构)
2. [数据库设计](#二数据库设计)
3. [核心引擎实现](#三核心引擎实现)
4. [API接口设计](#四api接口设计)
5. [前端架构](#五前端架构)
6. [部署方案](#六部署方案)
7. [开发规范](#七开发规范)

---

## 一、项目目录结构

```
HAXAtom/
├── backend/                          # 后端项目根目录
│   ├── app/                          # 应用主包
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI应用入口
│   │   ├── config.py                 # 全局配置管理
│   │   ├── dependencies.py           # FastAPI依赖注入
│   │   │
│   │   ├── api/                      # API路由层
│   │   │   ├── __init__.py
│   │   │   ├── v1/                   # API版本v1
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py         # 模型配置API
│   │   │   │   ├── prompts.py        # 提示词配置API
│   │   │   │   ├── plugins.py        # 插件配置API
│   │   │   │   ├── knowledge_bases.py # 知识库API
│   │   │   │   ├── memories.py       # 记忆配置API
│   │   │   │   ├── presets.py        # 预设方案API
│   │   │   │   ├── chat.py           # 对话API
│   │   │   │   └── system.py         # 系统管理API
│   │   │   └── deps.py               # API依赖
│   │   │
│   │   ├── core/                     # 核心引擎层
│   │   │   ├── __init__.py
│   │   │   ├── preset_engine.py      # 预设组合引擎
│   │   │   ├── langgraph_workflow.py # LangGraph工作流定义
│   │   │   ├── lcel_chains.py        # LCEL链定义
│   │   │   ├── rag_engine.py         # RAG检索引擎
│   │   │   ├── tool_engine.py        # 工具调用引擎
│   │   │   └── memory_manager.py     # 记忆管理器
│   │   │
│   │   ├── models/                   # 数据模型层
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # SQLAlchemy基类
│   │   │   ├── model_config.py       # 模型配置表
│   │   │   ├── prompt_config.py      # 提示词配置表
│   │   │   ├── plugin_config.py      # 插件配置表
│   │   │   ├── knowledge_base.py     # 知识库配置表
│   │   │   ├── memory_config.py      # 记忆配置表
│   │   │   ├── preset.py             # 预设方案表
│   │   │   ├── conversation.py       # 对话历史表
│   │   │   └── user.py               # 用户表
│   │   │
│   │   ├── schemas/                  # Pydantic模型层
│   │   │   ├── __init__.py
│   │   │   ├── model_config.py       # 模型配置Schema
│   │   │   ├── prompt_config.py      # 提示词配置Schema
│   │   │   ├── plugin_config.py      # 插件配置Schema
│   │   │   ├── knowledge_base.py     # 知识库Schema
│   │   │   ├── memory_config.py      # 记忆配置Schema
│   │   │   ├── preset.py             # 预设方案Schema
│   │   │   ├── chat.py               # 对话相关Schema
│   │   │   └── common.py             # 通用Schema
│   │   │
│   │   ├── services/                 # 业务逻辑层
│   │   │   ├── __init__.py
│   │   │   ├── model_pool.py         # 模型池服务
│   │   │   ├── prompt_pool.py        # 提示词池服务
│   │   │   ├── plugin_pool.py        # 插件池服务
│   │   │   ├── knowledge_pool.py     # 知识库池服务
│   │   │   ├── memory_pool.py        # 记忆池服务
│   │   │   ├── preset_service.py     # 预设方案服务
│   │   │   └── chat_service.py       # 对话服务
│   │   │
│   │   ├── db/                       # 数据库层
│   │   │   ├── __init__.py
│   │   │   ├── session.py            # 数据库会话管理
│   │   │   └── migrations/           # Alembic迁移文件
│   │   │
│   │   ├── plugins/                  # 插件目录
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # 插件基类
│   │   │   ├── registry.py           # 插件注册表
│   │   │   ├── web_search.py         # 联网搜索插件
│   │   │   ├── weather.py            # 天气查询插件
│   │   │   └── ...                   # 其他插件
│   │   │
│   │   ├── vectorstore/              # 向量存储层
│   │   │   ├── __init__.py
│   │   │   ├── chroma_manager.py     # ChromaDB管理器
│   │   │   └── embeddings.py         # 嵌入模型管理
│   │   │
│   │   ├── utils/                    # 工具函数
│   │   │   ├── __init__.py
│   │   │   ├── crypto.py             # 加密工具
│   │   │   ├── yaml_utils.py         # YAML处理
│   │   │   └── validators.py         # 自定义校验器
│   │   │
│   │   └── observability/            # 可观测性层
│   │       ├── __init__.py
│   │       ├── langsmith_client.py   # LangSmith客户端
│   │       └── tracing.py            # 追踪装饰器
│   │
│   ├── tests/                        # 测试目录
│   │   ├── __init__.py
│   │   ├── conftest.py               # pytest配置
│   │   ├── test_api/                 # API测试
│   │   ├── test_core/                # 核心引擎测试
│   │   └── test_services/            # 服务层测试
│   │
│   ├── alembic.ini                   # Alembic配置
│   ├── pyproject.toml                # Poetry依赖配置
│   ├── poetry.lock                   # 锁定依赖版本
│   ├── .env.example                  # 环境变量示例
│   └── Dockerfile                    # Docker构建文件
│
├── frontend/                         # 前端项目根目录
│   ├── src/
│   │   ├── components/               # 公共组件
│   │   │   ├── common/               # 通用组件
│   │   │   ├── layout/               # 布局组件
│   │   │   └── chat/                 # 对话相关组件
│   │   │
│   │   ├── views/                    # 页面视图
│   │   │   ├── bot/                  # Bot管理端视图
│   │   │   │   ├── ModelManager.vue
│   │   │   │   ├── PromptManager.vue
│   │   │   │   ├── PluginManager.vue
│   │   │   │   ├── KnowledgeManager.vue
│   │   │   │   ├── MemoryManager.vue
│   │   │   │   └── PresetManager.vue
│   │   │   │
│   │   │   ├── chat/                 # Chat对话端视图
│   │   │   │   ├── ChatView.vue
│   │   │   │   ├── PresetSelector.vue
│   │   │   │   ├── MessageList.vue
│   │   │   │   └── InputArea.vue
│   │   │   │
│   │   │   └── system/               # 系统管理视图
│   │   │
│   │   ├── api/                      # API接口封装
│   │   │   ├── index.ts
│   │   │   ├── models.ts
│   │   │   ├── presets.ts
│   │   │   └── chat.ts
│   │   │
│   │   ├── stores/                   # Pinia状态管理
│   │   │   ├── index.ts
│   │   │   ├── preset.ts             # 预设方案状态
│   │   │   ├── chat.ts               # 对话状态
│   │   │   └── user.ts               # 用户状态
│   │   │
│   │   ├── router/                   # Vue Router配置
│   │   │   └── index.ts
│   │   │
│   │   ├── utils/                    # 工具函数
│   │   │   ├── request.ts            # HTTP请求封装
│   │   │   ├── sse.ts                # SSE流式处理
│   │   │   └── format.ts             # 格式化工具
│   │   │
│   │   ├── types/                    # TypeScript类型定义
│   │   │   ├── model.ts
│   │   │   ├── preset.ts
│   │   │   └── chat.ts
│   │   │
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── style.css
│   │
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── tailwind.config.js
│
├── data/                             # 数据目录（运行时生成）
│   ├── db/                           # SQLite数据库文件
│   ├── chroma/                       # ChromaDB向量数据
│   ├── uploads/                      # 上传文件临时存储
│   └── backups/                      # 配置备份
│
├── docs/                             # 项目文档
│   ├── api.md                        # API文档
│   ├── plugin_dev.md                 # 插件开发指南
│   └── deployment.md                 # 部署指南
│
├── scripts/                          # 工具脚本
│   ├── build_exe.py                  # 打包exe脚本
│   ├── init_db.py                    # 数据库初始化
│   └── backup.py                     # 备份脚本
│
├── docker-compose.yml                # Docker Compose配置
├── .gitignore
├── LICENSE
└── README.md
```

---

## 二、数据库设计

### 2.1 数据库模型关系图

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  model_configs  │     │  prompt_configs │     │ plugin_configs  │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │     │ id (PK)         │
│ model_id (UQ)   │     │ prompt_id (UQ)  │     │ plugin_id (UQ)  │
│ model_name      │     │ prompt_name     │     │ plugin_name     │
│ provider        │     │ system_prompt   │     │ class_name      │
│ api_base        │     │ variables       │     │ plugin_params   │
│ api_key         │     │ ...             │     │ ...             │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │         presets           │
                    ├───────────────────────────┤
                    │ id (PK)                   │
                    │ preset_id (UQ)            │
                    │ preset_name               │
                    │ selected_model (FK)       │
                    │ selected_prompt (FK)      │
                    │ selected_plugins (JSON)   │
                    │ selected_knowledge_bases  │
                    │ selected_memory (FK)      │
                    │ overrides (JSON)          │
                    │ channel_config (JSON)     │
                    └───────────────────────────┘
                                 │
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌────────▼─────────┐    ┌────────▼─────────┐    ┌────────▼─────────┐
│knowledge_bases   │    │  memory_configs  │    │  conversations   │
├──────────────────┤    ├──────────────────┤    ├──────────────────┤
│ id (PK)          │    │ id (PK)          │    │ id (PK)          │
│ kb_id (UQ)       │    │ memory_id (UQ)   │    │ preset_id (FK)   │
│ kb_name          │    │ memory_name      │    │ session_id       │
│ embedding_model  │    │ memory_type      │    │ messages (JSON)  │
│ retrieval_params │    │ memory_params    │    │ created_at       │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

### 2.2 详细表结构

#### model_configs 模型配置表

```sql
CREATE TABLE model_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id VARCHAR(64) UNIQUE NOT NULL,      -- 唯一标识，如 model_deepseek_v3
    model_name VARCHAR(128) NOT NULL,          -- 显示名称
    model_type VARCHAR(32) NOT NULL,           -- chat/embedding
    provider VARCHAR(32) NOT NULL,             -- openai/deepseek/ollama
    api_base VARCHAR(256),                     -- API基础URL
    api_key VARCHAR(512),                      -- 加密存储的API Key
    default_params JSON,                       -- 默认参数 {temperature, max_tokens...}
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### prompt_configs 提示词配置表

```sql
CREATE TABLE prompt_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id VARCHAR(64) UNIQUE NOT NULL,     -- 唯一标识
    prompt_name VARCHAR(128) NOT NULL,         -- 显示名称
    system_prompt TEXT NOT NULL,               -- 系统提示词内容
    variables JSON,                            -- 变量列表 ["user_name", ...]
    temperature_override FLOAT,                -- 可选的温度覆盖
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### plugin_configs 插件配置表

```sql
CREATE TABLE plugin_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plugin_id VARCHAR(64) UNIQUE NOT NULL,     -- 唯一标识
    plugin_name VARCHAR(128) NOT NULL,         -- 显示名称
    class_name VARCHAR(128) NOT NULL,          -- 插件类名
    module_path VARCHAR(256),                  -- 模块路径
    plugin_params JSON,                        -- 插件参数
    config_schema JSON,                        -- 参数JSON Schema
    permission_level INTEGER DEFAULT 1,        -- 权限等级
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### knowledge_bases 知识库配置表

```sql
CREATE TABLE knowledge_bases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kb_id VARCHAR(64) UNIQUE NOT NULL,         -- 唯一标识
    kb_name VARCHAR(128) NOT NULL,             -- 显示名称
    description TEXT,                          -- 描述
    collection_name VARCHAR(64) NOT NULL,      -- ChromaDB集合名
    embedding_model VARCHAR(64) NOT NULL,      -- 使用的嵌入模型ID
    retrieval_params JSON,                     -- 检索参数
    document_count INTEGER DEFAULT 0,          -- 文档数量
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### memory_configs 记忆配置表

```sql
CREATE TABLE memory_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_id VARCHAR(64) UNIQUE NOT NULL,     -- 唯一标识
    memory_name VARCHAR(128) NOT NULL,         -- 显示名称
    memory_type VARCHAR(32) NOT NULL,          -- buffer_window/summary/vector
    memory_params JSON,                        -- 记忆参数
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### presets 预设方案表

```sql
CREATE TABLE presets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    preset_id VARCHAR(64) UNIQUE NOT NULL,     -- 唯一标识
    preset_name VARCHAR(128) NOT NULL,         -- 显示名称
    description TEXT,                          -- 描述
    selected_model VARCHAR(64) NOT NULL,       -- 引用的模型ID
    selected_prompt VARCHAR(64),               -- 引用的提示词ID
    selected_plugins JSON,                     -- 引用的插件ID列表
    selected_knowledge_bases JSON,             -- 引用的知识库ID列表
    selected_memory VARCHAR(64),               -- 引用的记忆ID
    overrides JSON,                            -- 覆盖配置
    channel_config JSON,                       -- 渠道配置
    is_default BOOLEAN DEFAULT 0,              -- 是否默认预设
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (selected_model) REFERENCES model_configs(model_id),
    FOREIGN KEY (selected_prompt) REFERENCES prompt_configs(prompt_id),
    FOREIGN KEY (selected_memory) REFERENCES memory_configs(memory_id)
);
```

#### conversations 对话历史表

```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(64) NOT NULL,           -- 会话ID
    preset_id VARCHAR(64) NOT NULL,            -- 使用的预设方案
    title VARCHAR(256),                        -- 对话标题（自动生成）
    messages JSON NOT NULL,                    -- 消息列表
    message_count INTEGER DEFAULT 0,           -- 消息数量
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (preset_id) REFERENCES presets(preset_id)
);

CREATE INDEX idx_conversations_preset ON conversations(preset_id);
CREATE INDEX idx_conversations_session ON conversations(session_id);
```

---

## 三、核心引擎实现

### 3.1 预设组合引擎 (Preset Engine)

预设组合引擎是项目的核心，负责根据预设方案动态组装LangGraph工作流。

```python
# backend/app/core/preset_engine.py

from typing import Any, Dict, Optional, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage

from app.schemas.preset import PresetConfig
from app.services.model_pool import ModelPool
from app.services.prompt_pool import PromptPool
from app.services.plugin_pool import PluginPool
from app.services.knowledge_pool import KnowledgePool
from app.services.memory_pool import MemoryPool


class AgentState(dict):
    """LangGraph状态定义"""
    messages: List[BaseMessage]
    preset_id: str
    context: Optional[str]
    tool_calls: Optional[List[Dict]]
    tool_results: Optional[List[Dict]]
    final_response: Optional[str]


class PresetEngine:
    """
    预设组合引擎
    
    核心职责：
    1. 根据preset_id加载完整配置
    2. 动态组装LangGraph工作流
    3. 管理对话状态与记忆
    """
    
    def __init__(self):
        self.model_pool = ModelPool()
        self.prompt_pool = PromptPool()
        self.plugin_pool = PluginPool()
        self.knowledge_pool = KnowledgePool()
        self.memory_pool = MemoryPool()
        self._workflows: Dict[str, StateGraph] = {}
    
    async def build_workflow(self, preset_id: str) -> StateGraph:
        """
        构建LangGraph工作流
        
        工作流结构：
        start -> [knowledge_retrieval] -> agent -> [tool_call] -> agent -> end
                      ↓                                    ↑
                   (可选)                              (循环)
        """
        preset = await self._load_preset(preset_id)
        
        # 初始化状态图
        workflow = StateGraph(AgentState)
        
        # 1. 添加知识检索节点（如果配置了知识库）
        if preset.selected_knowledge_bases:
            workflow.add_node(
                "knowledge_retrieval",
                self._create_knowledge_node(preset)
            )
        
        # 2. 添加Agent主节点
        workflow.add_node(
            "agent",
            self._create_agent_node(preset)
        )
        
        # 3. 添加工具调用节点（如果配置了插件）
        if preset.selected_plugins:
            workflow.add_node(
                "tools",
                self._create_tool_node(preset)
            )
        
        # 4. 设置入口点
        entry_point = "knowledge_retrieval" if preset.selected_knowledge_bases else "agent"
        workflow.set_entry_point(entry_point)
        
        # 5. 添加边
        if preset.selected_knowledge_bases:
            workflow.add_edge("knowledge_retrieval", "agent")
        
        # 6. 添加条件边：判断是否需要调用工具
        if preset.selected_plugins:
            workflow.add_conditional_edges(
                "agent",
                self._should_call_tools,
                {
                    "continue": "tools",
                    "end": END
                }
            )
            workflow.add_edge("tools", "agent")
        else:
            workflow.add_edge("agent", END)
        
        # 7. 编译并添加检查点（用于记忆持久化）
        checkpointer = MemorySaver()
        compiled = workflow.compile(checkpointer=checkpointer)
        
        self._workflows[preset_id] = compiled
        return compiled
    
    async def _load_preset(self, preset_id: str) -> PresetConfig:
        """加载预设方案及所有关联配置"""
        # 实现从数据库加载预设配置
        pass
    
    def _create_knowledge_node(self, preset: PresetConfig):
        """创建知识检索节点"""
        from app.core.rag_engine import RAGEngine
        
        rag_engine = RAGEngine(preset.selected_knowledge_bases)
        
        async def knowledge_node(state: AgentState) -> AgentState:
            query = state["messages"][-1].content
            context = await rag_engine.retrieve(query)
            state["context"] = context
            return state
        
        return knowledge_node
    
    def _create_agent_node(self, preset: PresetConfig):
        """创建Agent主节点"""
        from app.core.lcel_chains import build_agent_chain
        
        chain = build_agent_chain(preset)
        
        async def agent_node(state: AgentState) -> AgentState:
            config = RunnableConfig(
                configurable={
                    "session_id": state.get("session_id"),
                    "preset_id": preset.preset_id
                }
            )
            response = await chain.ainvoke(state, config)
            state["messages"].append(response)
            return state
        
        return agent_node
    
    def _create_tool_node(self, preset: PresetConfig):
        """创建工具调用节点"""
        from langgraph.prebuilt import ToolNode
        from app.core.tool_engine import ToolEngine
        
        tool_engine = ToolEngine(preset.selected_plugins)
        tools = tool_engine.get_tools()
        
        return ToolNode(tools)
    
    def _should_call_tools(self, state: AgentState) -> str:
        """判断是否需要调用工具"""
        last_message = state["messages"][-1]
        
        # 检查是否有工具调用请求
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"
        return "end"
    
    async def chat(
        self,
        preset_id: str,
        message: str,
        session_id: str,
        stream: bool = True
    ):
        """
        执行对话
        
        Args:
            preset_id: 预设方案ID
            message: 用户消息
            session_id: 会话ID（用于记忆隔离）
            stream: 是否流式输出
        """
        # 获取或构建工作流
        if preset_id not in self._workflows:
            await self.build_workflow(preset_id)
        
        workflow = self._workflows[preset_id]
        
        # 初始化状态
        initial_state = AgentState(
            messages=[{"role": "user", "content": message}],
            preset_id=preset_id,
            context=None,
            tool_calls=None,
            tool_results=None,
            final_response=None
        )
        
        # 执行工作流
        config = {"configurable": {"thread_id": session_id}}
        
        if stream:
            async for event in workflow.astream_events(initial_state, config, version="v1"):
                yield event
        else:
            result = await workflow.ainvoke(initial_state, config)
            yield result
```

### 3.2 LCEL链定义

```python
# backend/app/core/lcel_chains.py

from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableConfig
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage

from app.schemas.preset import PresetConfig


def build_agent_chain(preset: PresetConfig):
    """
    构建Agent对话链
    
    链结构：
    输入 -> 提示词模板 -> 模型 -> 输出解析
    """
    
    # 1. 构建系统提示词
    system_prompt = build_system_prompt(preset)
    
    # 2. 构建提示词模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    # 3. 获取模型实例
    model = build_model(preset)
    
    # 4. 组装LCEL链
    chain = (
        RunnablePassthrough.assign(
            # 注入对话历史
            chat_history=lambda x: get_chat_history(x.get("session_id")),
            # 注入知识上下文（如果有）
            input=lambda x: build_input_with_context(x)
        )
        | prompt
        | model
        | StrOutputParser()
    )
    
    # 5. 添加LangSmith追踪配置
    chain = chain.with_config({
        "run_name": f"preset_{preset.preset_id}",
        "tags": ["agent", preset.preset_id],
        "metadata": {
            "preset_id": preset.preset_id,
            "model": preset.selected_model
        }
    })
    
    return chain


def build_system_prompt(preset: PresetConfig) -> str:
    """构建系统提示词"""
    from app.services.prompt_pool import PromptPool
    
    prompt_pool = PromptPool()
    prompt_config = prompt_pool.get(preset.selected_prompt)
    
    system_prompt = prompt_config.system_prompt
    
    # 注入知识上下文占位符（如果有知识库）
    if preset.selected_knowledge_bases:
        system_prompt += "\n\n相关上下文：{context}"
    
    return system_prompt


def build_model(preset: PresetConfig):
    """构建模型实例"""
    from app.services.model_pool import ModelPool
    
    model_pool = ModelPool()
    model_config = model_pool.get(preset.selected_model)
    
    # 根据provider创建对应模型实例
    if model_config.provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model_config.model_id,
            api_key=model_config.api_key,
            base_url=model_config.api_base,
            **model_config.default_params
        )
    elif model_config.provider == "deepseek":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="deepseek-chat",
            api_key=model_config.api_key,
            base_url=model_config.api_base,
            **model_config.default_params
        )
    elif model_config.provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=model_config.model_id,
            base_url=model_config.api_base,
            **model_config.default_params
        )
    else:
        raise ValueError(f"Unknown provider: {model_config.provider}")


def get_chat_history(session_id: str):
    """获取对话历史"""
    # 从数据库加载对话历史
    pass


def build_input_with_context(state: dict) -> str:
    """构建带上下文的输入"""
    user_input = state["messages"][-1]["content"]
    context = state.get("context")
    
    if context:
        return f"基于以下上下文回答问题：\n{context}\n\n用户问题：{user_input}"
    return user_input
```

### 3.3 RAG检索引擎

```python
# backend/app/core/rag_engine.py

from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

from app.vectorstore.chroma_manager import ChromaManager


class RAGEngine:
    """
    RAG检索引擎
    
    支持多知识库联合检索、重排序、结果合并
    """
    
    def __init__(self, kb_ids: List[str]):
        self.kb_ids = kb_ids
        self.chroma_manager = ChromaManager()
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 4,
        search_type: str = "mmr"
    ) -> str:
        """
        执行检索
        
        Args:
            query: 查询语句
            top_k: 返回文档数
            search_type: 检索类型 (similarity/mmr)
        
        Returns:
            合并后的上下文文本
        """
        all_docs = []
        
        # 1. 从多个知识库并行检索
        for kb_id in self.kb_ids:
            retriever = self.chroma_manager.get_retriever(
                kb_id=kb_id,
                search_type=search_type,
                k=top_k
            )
            docs = await retriever.aretrieve(query)
            all_docs.extend(docs)
        
        # 2. 去重（按内容相似度）
        unique_docs = self._deduplicate(all_docs)
        
        # 3. 重排序（如果有配置）
        ranked_docs = await self._rerank(query, unique_docs)
        
        # 4. 格式化上下文
        context = self._format_context(ranked_docs[:top_k])
        
        return context
    
    def _deduplicate(self, docs: List[Document]) -> List[Document]:
        """基于内容相似度去重"""
        seen = set()
        unique = []
        
        for doc in docs:
            # 使用内容哈希去重
            content_hash = hash(doc.page_content[:100])
            if content_hash not in seen:
                seen.add(content_hash)
                unique.append(doc)
        
        return unique
    
    async def _rerank(
        self,
        query: str,
        docs: List[Document]
    ) -> List[Document]:
        """
        重排序
        
        可选方案：
        1. 使用重排序模型（如bge-reranker）
        2. 使用LLM进行相关性打分
        """
        # TODO: 实现重排序逻辑
        return docs
    
    def _format_context(self, docs: List[Document]) -> str:
        """格式化检索结果为上下文"""
        contexts = []
        
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "未知来源")
            contexts.append(f"[{i}] 来源：{source}\n{doc.page_content}")
        
        return "\n\n".join(contexts)
    
    async def add_documents(
        self,
        kb_id: str,
        documents: List[Document]
    ):
        """向知识库添加文档"""
        await self.chroma_manager.add_documents(kb_id, documents)
```

### 3.4 工具调用引擎

```python
# backend/app/core/tool_engine.py

from typing import List, Type, Any
from langchain_core.tools import BaseTool

from app.plugins.base import BasePlugin
from app.plugins.registry import PluginRegistry


class ToolEngine:
    """
    工具调用引擎
    
    负责动态加载插件并转换为LangChain工具
    """
    
    def __init__(self, plugin_ids: List[str]):
        self.plugin_ids = plugin_ids
        self.registry = PluginRegistry()
        self._tools: List[BaseTool] = []
    
    def load_plugins(self):
        """加载所有配置的插件"""
        for plugin_id in self.plugin_ids:
            plugin_class = self.registry.get(plugin_id)
            if plugin_class:
                plugin = plugin_class()
                tool = plugin.to_langchain_tool()
                self._tools.append(tool)
    
    def get_tools(self) -> List[BaseTool]:
        """获取所有工具实例"""
        if not self._tools:
            self.load_plugins()
        return self._tools


# backend/app/plugins/base.py

from abc import ABC, abstractmethod
from typing import Any, Dict
from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel, Field


class BasePlugin(ABC):
    """
    插件基类
    
    所有插件必须继承此类
    """
    
    # 插件元数据
    name: str = ""
    description: str = ""
    args_schema: Type[BaseModel] = None
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
    
    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """
        执行插件逻辑
        
        Returns:
            执行结果文本
        """
        pass
    
    def to_langchain_tool(self) -> BaseTool:
        """转换为LangChain工具"""
        return StructuredTool.from_function(
            name=self.name,
            description=self.description,
            func=self.execute,
            args_schema=self.args_schema,
            coroutine=self.execute
        )


# backend/app/plugins/web_search.py

from pydantic import BaseModel, Field
from app.plugins.base import BasePlugin


class WebSearchInput(BaseModel):
    """联网搜索输入参数"""
    query: str = Field(description="搜索关键词")
    num_results: int = Field(default=3, description="返回结果数量")


class WebSearchPlugin(BasePlugin):
    """联网搜索插件"""
    
    name = "web_search"
    description = "使用搜索引擎查询最新信息"
    args_schema = WebSearchInput
    
    async def execute(self, query: str, num_results: int = 3) -> str:
        """执行搜索"""
        # 实现搜索逻辑
        # 可以使用Serper API、Bing API等
        search_engine = self.config.get("search_engine", "google")
        
        # 示例实现
        results = await self._search(query, num_results)
        return self._format_results(results)
    
    async def _search(self, query: str, num: int) -> list:
        # 实际搜索实现
        pass
    
    def _format_results(self, results: list) -> str:
        # 格式化搜索结果
        pass
```

### 3.5 记忆管理器

```python
# backend/app/core/memory_manager.py

from typing import List, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.models.conversation import Conversation
from app.db.session import async_session


class ConversationHistory(BaseChatMessageHistory):
    """
    自定义对话历史管理器
    
    基于数据库存储，支持多会话隔离
    """
    
    def __init__(self, session_id: str, preset_id: str):
        self.session_id = session_id
        self.preset_id = preset_id
        self._messages: List[BaseMessage] = []
    
    @property
    def messages(self) -> List[BaseMessage]:
        """获取消息列表"""
        if not self._messages:
            self._load_from_db()
        return self._messages
    
    def add_message(self, message: BaseMessage) -> None:
        """添加消息"""
        self._messages.append(message)
        self._save_to_db()
    
    def clear(self) -> None:
        """清空历史"""
        self._messages = []
        self._clear_db()
    
    def _load_from_db(self):
        """从数据库加载"""
        # 实现数据库查询
        pass
    
    def _save_to_db(self):
        """保存到数据库"""
        # 实现数据库保存
        pass
    
    def _clear_db(self):
        """清空数据库记录"""
        # 实现数据库清空
        pass


class MemoryManager:
    """
    记忆管理器
    
    管理不同预设方案的对话历史
    """
    
    def __init__(self):
        self._histories: Dict[str, ConversationHistory] = {}
    
    def get_history(
        self,
        session_id: str,
        preset_id: str
    ) -> ConversationHistory:
        """获取或创建对话历史"""
        key = f"{preset_id}:{session_id}"
        
        if key not in self._histories:
            self._histories[key] = ConversationHistory(session_id, preset_id)
        
        return self._histories[key]
    
    def clear_history(self, session_id: str, preset_id: str):
        """清空指定会话历史"""
        key = f"{preset_id}:{session_id}"
        
        if key in self._histories:
            self._histories[key].clear()
            del self._histories[key]


# 全局记忆管理器实例
memory_manager = MemoryManager()


def get_session_history(session_id: str, preset_id: str) -> BaseChatMessageHistory:
    """获取会话历史的工厂函数"""
    return memory_manager.get_history(session_id, preset_id)
```

---

## 四、API接口设计

### 4.1 RESTful API规范

所有API遵循RESTful规范，统一返回格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": 1712345678
}
```

### 4.2 核心API列表

#### 模型配置API

```yaml
# 模型配置管理
GET    /api/v1/models              # 获取模型列表
POST   /api/v1/models              # 创建模型配置
GET    /api/v1/models/{model_id}   # 获取模型详情
PUT    /api/v1/models/{model_id}   # 更新模型配置
DELETE /api/v1/models/{model_id}   # 删除模型配置
POST   /api/v1/models/{model_id}/test  # 测试模型连接
```

#### 预设方案API

```yaml
# 预设方案管理
GET    /api/v1/presets              # 获取预设列表
POST   /api/v1/presets              # 创建预设方案
GET    /api/v1/presets/{preset_id}  # 获取预设详情
PUT    /api/v1/presets/{preset_id}  # 更新预设方案
DELETE /api/v1/presets/{preset_id}  # 删除预设方案
POST   /api/v1/presets/{preset_id}/clone  # 克隆预设方案
POST   /api/v1/presets/{preset_id}/export # 导出预设配置
POST   /api/v1/presets/import       # 导入预设配置
```

#### 对话API

```yaml
# 对话管理
POST   /api/v1/chat                 # 发送消息（非流式）
POST   /api/v1/chat/stream          # 发送消息（流式SSE）
POST   /api/v1/chat/{session_id}/stop  # 停止生成
DELETE /api/v1/chat/{session_id}    # 清空对话
GET    /api/v1/chat/history         # 获取对话历史列表
GET    /api/v1/chat/history/{session_id}  # 获取指定对话详情
```

#### 知识库API

```yaml
# 知识库管理
GET    /api/v1/knowledge            # 获取知识库列表
POST   /api/v1/knowledge            # 创建知识库
GET    /api/v1/knowledge/{kb_id}    # 获取知识库详情
PUT    /api/v1/knowledge/{kb_id}    # 更新知识库
DELETE /api/v1/knowledge/{kb_id}    # 删除知识库
POST   /api/v1/knowledge/{kb_id}/documents      # 上传文档
DELETE /api/v1/knowledge/{kb_id}/documents/{doc_id}  # 删除文档
POST   /api/v1/knowledge/{kb_id}/search         # 测试检索
```

### 4.3 核心API实现示例

```python
# backend/app/api/v1/chat.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

from app.core.preset_engine import PresetEngine
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/chat")
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends()
) -> ChatResponse:
    """
    非流式对话
    """
    response = await chat_service.chat(
        preset_id=request.preset_id,
        message=request.message,
        session_id=request.session_id
    )
    return ChatResponse(
        code=200,
        message="success",
        data={"content": response}
    )


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    chat_service: ChatService = Depends()
):
    """
    流式对话（SSE）
    """
    async def event_generator():
        async for chunk in chat_service.chat_stream(
            preset_id=request.preset_id,
            message=request.message,
            session_id=request.session_id
        ):
            yield {
                "event": "message",
                "data": chunk
            }
        
        # 发送结束标记
        yield {
            "event": "done",
            "data": "[DONE]"
        }
    
    return EventSourceResponse(event_generator())


@router.get("/chat/history")
async def get_chat_history(
    preset_id: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    chat_service: ChatService = Depends()
):
    """
    获取对话历史列表
    """
    histories = await chat_service.get_history_list(
        preset_id=preset_id,
        page=page,
        page_size=page_size
    )
    return {"code": 200, "data": histories}
```

---

## 五、前端架构

### 5.1 前端目录结构

```
frontend/src/
├── components/           # 组件目录
│   ├── common/          # 通用组件
│   │   ├── AppHeader.vue
│   │   ├── AppSidebar.vue
│   │   ├── DataTable.vue
│   │   └── FormDialog.vue
│   │
│   ├── chat/            # 对话组件
│   │   ├── ChatContainer.vue    # 对话容器
│   │   ├── MessageList.vue      # 消息列表
│   │   ├── MessageItem.vue      # 单条消息
│   │   ├── InputArea.vue        # 输入区域
│   │   ├── PresetSelector.vue   # 预设选择器
│   │   └── StreamingText.vue    # 流式文本渲染
│   │
│   └── config/          # 配置管理组件
│       ├── ModelForm.vue
│       ├── PromptForm.vue
│       ├── PluginCard.vue
│       └── PresetBuilder.vue    # 预设拼装器
│
├── views/               # 页面视图
│   ├── Layout.vue       # 主布局
│   ├── bot/             # Bot管理端
│   │   ├── Dashboard.vue
│   │   ├── ModelManager.vue
│   │   ├── PromptManager.vue
│   │   ├── PluginManager.vue
│   │   ├── KnowledgeManager.vue
│   │   ├── MemoryManager.vue
│   │   └── PresetManager.vue
│   │
│   ├── chat/            # Chat对话端
│   │   └── ChatView.vue
│   │
│   └── system/          # 系统管理
│       ├── Settings.vue
│       └── Logs.vue
│
├── api/                 # API封装
│   ├── index.ts         # axios实例
│   ├── models.ts
│   ├── presets.ts
│   ├── chat.ts
│   └── knowledge.ts
│
├── stores/              # Pinia状态管理
│   ├── index.ts
│   ├── app.ts           # 应用状态
│   ├── preset.ts        # 预设方案状态
│   ├── chat.ts          # 对话状态
│   └── user.ts
│
├── composables/         # 组合式函数
│   ├── useSSE.ts        # SSE流式处理
│   ├── useChat.ts       # 对话逻辑
│   └── useConfig.ts     # 配置管理
│
├── router/              # 路由配置
│   └── index.ts
│
├── utils/               # 工具函数
│   ├── format.ts
│   ├── storage.ts
│   └── validators.ts
│
└── types/               # TypeScript类型
    ├── model.ts
    ├── preset.ts
    └── chat.ts
```

### 5.2 核心组件实现

#### 预设选择器组件

```vue
<!-- frontend/src/components/chat/PresetSelector.vue -->
<template>
  <div class="preset-selector">
    <el-select
      v-model="selectedPreset"
      placeholder="选择预设方案"
      @change="handlePresetChange"
      class="w-full"
    >
      <el-option
        v-for="preset in presetStore.presets"
        :key="preset.preset_id"
        :label="preset.preset_name"
        :value="preset.preset_id"
      >
        <div class="preset-option">
          <span class="name">{{ preset.preset_name }}</span>
          <span class="model">{{ preset.selected_model }}</span>
        </div>
      </el-option>
    </el-select>
    
    <!-- 预设详情展示 -->
    <div v-if="currentPreset" class="preset-info">
      <el-tag size="small">{{ currentPreset.selected_model }}</el-tag>
      <el-tag size="small" v-if="currentPreset.selected_knowledge_bases?.length">
        知识库 {{ currentPreset.selected_knowledge_bases.length }}
      </el-tag>
      <el-tag size="small" v-if="currentPreset.selected_plugins?.length">
        插件 {{ currentPreset.selected_plugins.length }}
      </el-tag>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { usePresetStore } from '@/stores/preset'
import { useChatStore } from '@/stores/chat'

const presetStore = usePresetStore()
const chatStore = useChatStore()

const selectedPreset = ref('')

const currentPreset = computed(() => 
  presetStore.presets.find(p => p.preset_id === selectedPreset.value)
)

const handlePresetChange = (presetId: string) => {
  chatStore.switchPreset(presetId)
}

// 初始化加载预设列表
onMounted(() => {
  presetStore.loadPresets()
})
</script>
```

#### 流式对话组件

```vue
<!-- frontend/src/components/chat/ChatContainer.vue -->
<template>
  <div class="chat-container">
    <!-- 消息列表 -->
    <MessageList 
      :messages="chatStore.messages"
      :streaming="chatStore.isStreaming"
    />
    
    <!-- 输入区域 -->
    <InputArea
      v-model="inputMessage"
      :loading="chatStore.isStreaming"
      @send="handleSend"
      @stop="handleStop"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useSSE } from '@/composables/useSSE'
import MessageList from './MessageList.vue'
import InputArea from './InputArea.vue'

const chatStore = useChatStore()
const { connect, disconnect, isConnected } = useSSE()

const inputMessage = ref('')

const handleSend = async () => {
  if (!inputMessage.value.trim()) return
  
  const message = inputMessage.value
  inputMessage.value = ''
  
  // 添加用户消息到列表
  chatStore.addMessage({
    role: 'user',
    content: message
  })
  
  // 开始流式接收
  chatStore.setStreaming(true)
  
  try {
    await connect('/api/v1/chat/stream', {
      preset_id: chatStore.currentPresetId,
      message: message,
      session_id: chatStore.sessionId
    }, {
      onMessage: (chunk) => {
        chatStore.appendStreamingContent(chunk)
      },
      onDone: () => {
        chatStore.finalizeStreamingMessage()
        chatStore.setStreaming(false)
      },
      onError: (error) => {
        console.error('Stream error:', error)
        chatStore.setStreaming(false)
      }
    })
  } catch (error) {
    chatStore.setStreaming(false)
  }
}

const handleStop = () => {
  disconnect()
  chatStore.setStreaming(false)
}
</script>
```

#### SSE组合式函数

```typescript
// frontend/src/composables/useSSE.ts

import { ref } from 'vue'

interface SSEOptions {
  onMessage: (data: string) => void
  onDone?: () => void
  onError?: (error: Error) => void
}

export function useSSE() {
  const isConnected = ref(false)
  const eventSource = ref<EventSource | null>(null)

  const connect = async (
    url: string,
    body: Record<string, any>,
    options: SSEOptions
  ) => {
    // 使用fetch + ReadableStream实现SSE，支持POST请求体
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify(body)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()
    isConnected.value = true

    try {
      while (true) {
        const { done, value } = await reader!.read()
        
        if (done) {
          options.onDone?.()
          break
        }

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            
            if (data === '[DONE]') {
              options.onDone?.()
              isConnected.value = false
              return
            }

            try {
              const parsed = JSON.parse(data)
              options.onMessage(parsed.content || parsed)
            } catch {
              options.onMessage(data)
            }
          }
        }
      }
    } catch (error) {
      options.onError?.(error as Error)
    } finally {
      isConnected.value = false
      reader?.releaseLock()
    }
  }

  const disconnect = () => {
    isConnected.value = false
    // 中断fetch请求需要AbortController，这里简化处理
  }

  return {
    isConnected,
    connect,
    disconnect
  }
}
```

---

## 六、部署方案

### 6.1 开发环境启动

```bash
# 1. 克隆项目
git clone <repository>
cd HAXAtom

# 2. 后端环境配置
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install poetry
poetry install

# 3. 初始化数据库
alembic upgrade head
python scripts/init_db.py

# 4. 启动后端
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. 前端环境配置（新终端）
cd frontend
npm install

# 6. 启动前端
npm run dev

# 7. 访问
# 前端: http://localhost:5173
# 后端API: http://localhost:8000
# API文档: http://localhost:8000/docs
```

### 6.2 Docker部署

```dockerfile
# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# 安装 Poetry
RUN pip install poetry

# 复制依赖配置
COPY pyproject.toml poetry.lock ./

# 安装依赖（不使用虚拟环境）
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# 复制应用代码
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY alembic.ini ./

# 创建数据目录
RUN mkdir -p /app/data/db /app/data/chroma /app/data/uploads

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

```dockerfile
# frontend/Dockerfile

FROM node:20-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

```yaml
# docker-compose.yml

version: '3.8'

services:
  backend:
    build: ./backend
    container_name: haxatom-backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///app/data/db/haxatom.db
      - CHROMA_PERSIST_DIR=/app/data/chroma
      - LANGSMITH_TRACING=${LANGSMITH_TRACING:-false}
      - LANGSMITH_API_KEY=${LANGSMITH_API_KEY}
    restart: unless-stopped

  frontend:
    build: ./frontend
    container_name: haxatom-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

### 6.3 Windows EXE打包

```python
# scripts/build_exe.py

import PyInstaller.__main__
import os
import shutil

def build_exe():
    """打包Windows可执行文件"""
    
    # 清理旧构建
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # PyInstaller配置
    PyInstaller.__main__.run([
        'app/main.py',                    # 入口文件
        '--name=HAXAtom',                 # 应用名称
        '--onefile',                      # 单文件
        '--windowed',                     # 无控制台窗口
        '--icon=assets/icon.ico',         # 图标
        '--add-data=app;app',             # 包含app目录
        '--add-data=data;data',           # 包含数据目录
        '--hidden-import=uvicorn.logging',
        '--hidden-import=uvicorn.loops.auto',
        '--hidden-import=uvicorn.protocols.http.auto',
        '--hidden-import=uvicorn.protocols.websockets.auto',
        '--hidden-import=sqlalchemy.ext.asyncio',
        '--hidden-import=chromadb',
        '--collect-all=langchain',
        '--collect-all=langgraph',
    ])
    
    print("Build completed! Check the 'dist' folder.")

if __name__ == '__main__':
    build_exe()
```

---

## 七、开发规范

### 7.1 代码规范

#### Python规范

```python
# 1. 类型注解必须完整
from typing import Optional, List, Dict, Any

def process_data(
    input_data: Dict[str, Any],
    options: Optional[Dict] = None
) -> List[str]:
    """函数文档字符串"""
    pass

# 2. 异步函数统一使用async/await
async def fetch_data() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
        return response.json()

# 3. Pydantic模型用于所有数据验证
from pydantic import BaseModel, Field

class UserConfig(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=0, le=150)
    email: Optional[str] = Field(None, pattern=r"^\S+@\S+\.\S+$")
```

#### 前端规范

```typescript
// 1. 类型定义必须完整
interface PresetConfig {
  preset_id: string
  preset_name: string
  selected_model: string
  selected_prompt?: string
  selected_plugins?: string[]
}

// 2. 组合式函数使用统一命名
export function usePresetManager() {
  // ...
}

// 3. 组件Props使用TypeScript接口
interface Props {
  preset: PresetConfig
  loading?: boolean
  onSelect?: (id: string) => void
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})
```

### 7.2 Git提交规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

Type类型：

- `feat`: 新功能
- `fix`: 修复
- `docs`: 文档
- `style`: 格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

示例：

```
feat(preset): 添加预设方案克隆功能

- 支持一键克隆现有预设
- 自动复制所有关联配置
- 添加克隆历史记录

Closes #123
```

### 7.3 项目开发路线图

#### Phase 1: 核心架构 (Week 1-2)

- [ ] 项目脚手架搭建
- [ ] 数据库模型设计与迁移
- [ ] 基础CRUD API实现
- [ ] LangGraph工作流基础框架
- [ ] LangSmith集成

#### Phase 2: 核心功能 (Week 3-4)

- [ ] 模型池管理完整功能
- [ ] 提示词池管理完整功能
- [ ] 预设方案拼装引擎
- [ ] 基础对话功能（流式）
- [ ] 前端基础界面

#### Phase 3: RAG与插件 (Week 5-6)

- [ ] ChromaDB集成
- [ ] 文档上传与向量化
- [ ] RAG检索引擎
- [ ] 插件系统框架
- [ ] 内置插件实现（搜索、天气）

#### Phase 4: 完善与部署 (Week 7-8)

- [ ] 前端管理界面完整功能
- [ ] 多渠道适配框架
- [ ] Docker打包
- [ ] Windows EXE打包
- [ ] 文档完善

---

## 附录

### A. 环境变量配置

```bash
# .env 文件模板

# 应用配置
APP_NAME=HAXAtom
APP_VERSION=0.1.0
DEBUG=false
SECRET_KEY=your-secret-key-here

# 数据库
DATABASE_URL=sqlite:///data/db/haxatom.db

# 向量存储
CHROMA_PERSIST_DIR=data/chroma

# LangSmith可观测性（可选）
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=ls-your-api-key
LANGSMITH_PROJECT=haxatom

# 默认模型（可选）
DEFAULT_MODEL_PROVIDER=deepseek
DEFAULT_MODEL_API_KEY=sk-your-api-key
DEFAULT_MODEL_API_BASE=https://api.deepseek.com
```

### B. 快速启动命令

```bash
# 一键启动开发环境
make dev

# 运行测试
make test

# 构建Docker镜像
make docker-build

# 打包Windows EXE
make build-exe

# 数据库迁移
make migrate
make migrate-create msg="add new table"
```

---

## 附录：HAXAtom 原子化解耦架构图

```
┌─────────────────────────────────────────────────────────┐
│                    预设方案 (Preset)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │  聊天模型    │  │  人设提示词  │  │   知识库列表     │ │
│  │ zhipu_glm4  │  │  general_   │  │ [产品库, FAQ库] │ │
│  │             │  │  assistant  │  │                 │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
│  ┌─────────────┐  ┌─────────────┐                       │
│  │    插件     │  │    记忆     │                       │
│  │ [time, calc]│  │   short_term│                       │
│  └─────────────┘  └─────────────┘                       │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   知识库 A     │    │   知识库 B     │    │   知识库 C     │
│ 产品文档库      │    │  售后FAQ库     │    │  技术规范库     │
│               │    │               │    │               │
│ 嵌入模型:      │    │ 嵌入模型:      │    │ 嵌入模型:      │
│ zhipu_embed   │    │ zhipu_embed   │    │ bge_m3_local  │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌─────────────────┐
                    │   模型配置池      │
                    │ ┌─────────────┐ │
                    │ │ 聊天模型 x N │ │
                    │ │ 嵌入模型 x N │ │
                    │ └─────────────┘ │
                    └─────────────────┘
```

### 架构设计原则

1. **完全解耦**：五大资源池（模型、提示词、插件、知识库、记忆）独立配置
2. **灵活组合**：预设方案通过ID引用各资源，实现乐高式拼装
3. **资源复用**：
   - 一个嵌入模型 → 多个知识库共用
   - 一个知识库 → 多个预设方案共用
   - 一个提示词 → 多个预设方案共用
4. **原子化管理**：每个资源独立CRUD，互不影响

### 使用流程

```
1. 配置嵌入模型（model_type="embedding"）
        ↓
2. 创建知识库（选择嵌入模型）
        ↓
3. 上传文档 → 自动分块 → 向量化
        ↓
4. 配置预设方案（选择聊天模型 + 知识库 + 提示词 + 插件）
        ↓
5. 对话时自动检索知识库 + 工具调用
```

---

## 附录B：多平台会话存储架构

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      统一会话架构                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐ │
│  │   Web平台     │      │   QQ平台      │      │ 飞书平台  │ │
│  │  (网页聊天)   │      │  (QQ机器人)   │      │ (机器人)  │ │
│  └──────┬───────┘      └──────┬───────┘      └────┬─────┘ │
│         │                     │                    │       │
│         │ session_id          │ qq_session_id      │       │
│         │ (web_xxx)           │ (qq_group_xxx)     │       │
│         │                     │                    │       │
│         └─────────────────────┼────────────────────┘       │
│                               │                            │
│                    ┌──────────▼──────────┐                 │
│                    │   conversations     │                 │
│                    │   (对话历史表)       │                 │
│                    ├─────────────────────┤                 │
│                    │ - session_id        │                 │
│                    │ - channel_type      │  ← 平台类型      │
│                    │ - channel_id        │  ← 平台ID        │
│                    │ - preset_id         │                 │
│                    │ - messages          │  ← 消息列表      │
│                    │ - platform_config   │  ← 平台配置      │
│                    └─────────────────────┘                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 会话ID生成规则

| 平台 | 格式 | 示例 |
|------|------|------|
| Web | `web_{uuid}` | web_abc123def456 |
| QQ群聊 | `qq_group_{group_id}_{user_id}` | qq_group_123456_789 |
| QQ私聊 | `qq_private_{user_id}` | qq_private_123456 |
| 飞书 | `feishu_{user_id}` | feishu_ou_xxx |
| 钉钉 | `dingtalk_{user_id}` | dingtalk_xxx |
| Telegram | `tg_{chat_id}_{user_id}` | tg_123_456 |

### 数据流向

```
Web平台用户：
┌─────────┐    POST /chat/completions    ┌─────────────┐
│  用户   │ ────────────────────────────→ │  Web API    │
│ 浏览器   │                               │  (FastAPI)  │
└─────────┘                               └──────┬──────┘
     ↑                                           │
     │         返回AI回复                         │
     └───────────────────────────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │  session_id:    │
                    │  web_abc123     │
                    │  channel: web   │
                    └─────────────────┘
                              ↓
                    ┌─────────────────┐
                    │  conversations  │
                    │  表存储对话历史  │
                    └─────────────────┘

QQ平台用户：
┌─────────┐    QQ消息事件    ┌─────────────┐
│  QQ用户  │ ───────────────→ │  QQ适配器    │
│         │                   │  (go-cqhttp) │
└─────────┘                   └──────┬──────┘
     ↑                               │
     │         返回AI回复              │
     └───────────────────────────────┘
                    ↓
          ┌─────────────────┐
          │  session_id:    │
          │  qq_group_xxx   │
          │  channel: qq    │
          └─────────────────┘
                    ↓
          ┌─────────────────┐
          │  conversations  │
          │  表存储对话历史  │
          └─────────────────┘
```

### 设计优势

1. **统一存储**：所有平台对话存储在同一张表，便于管理和查询
2. **平台隔离**：通过 `channel_type` 和 `channel_id` 区分不同平台
3. **会话隔离**：不同平台使用不同前缀的 session_id，避免冲突
4. **灵活扩展**：新增平台只需添加新的 channel_type，无需改表结构

---

**文档版本**: v1.0  
**最后更新**: 2026-04-01  
**作者**: HAXAtom Team
