# HAXAtom 待完成功能清单

> 基于项目文档与代码深度分析整理
> 生成时间：2026-04-16

---

## 一、配置文件导入导出（P0）

### 1.1 需求背景

项目核心卖点是「乐高式拼装」，文档多次强调：
- 每个资源池配置可单独导出为 YAML/JSON
- 预设方案支持一键导出/导入/分享
- 当前代码未实现该能力

### 1.2 功能范围

| 模块 | 导出 | 导入 | 说明 |
|------|------|------|------|
| 模型配置池 | ✅ | ✅ | 单条/批量导出 |
| 提示词配置池 | ✅ | ✅ | 含变量定义 |
| 插件配置池 | ✅ | ✅ | 含参数配置 |
| 知识库配置 | ✅ | ✅ | 不含向量数据 |
| 记忆配置池 | ✅ | ✅ | 策略配置 |
| 预设方案 | ✅ | ✅ | 含所有资源引用 |

### 1.3 API 设计

```
GET    /api/v1/models/{model_id}/export          # 导出模型配置
POST   /api/v1/models/import                      # 导入模型配置
GET    /api/v1/prompts/{prompt_id}/export         # 导出提示词
POST   /api/v1/prompts/import                     # 导入提示词
GET    /api/v1/plugins/{plugin_id}/export         # 导出插件配置
POST   /api/v1/plugins/import                     # 导入插件配置
GET    /api/v1/knowledge-bases/{kb_id}/export     # 导出知识库配置
POST   /api/v1/knowledge-bases/import             # 导入知识库配置
GET    /api/v1/memories/{memory_id}/export        # 导出记忆配置
POST   /api/v1/memories/import                    # 导入记忆配置
GET    /api/v1/presets/{preset_id}/export         # 导出预设方案
POST   /api/v1/presets/import                     # 导入预设方案
```

### 1.4 导出格式示例

```yaml
# 预设方案导出示例
export_type: preset
export_version: "1.0"
export_time: "2026-04-16T10:30:00Z"

preset:
  preset_id: preset_tsundere_girlfriend_deepseek
  preset_name: 傲娇女友（DeepSeek-V3）
  description: 基于DeepSeek-V3模型的傲娇女友聊天Bot
  selected_model: model_deepseek_v3_chat
  selected_prompt: prompt_tsundere_girlfriend_v2
  selected_plugins:
    - plugin_web_search_baidu
  selected_knowledge_bases: []
  selected_memory: memory_short_term_10_rounds
  overrides:
    model_params:
      temperature: 0.9
  is_active: true

# 引用的资源一并导出（可选）
resources:
  models:
    - model_id: model_deepseek_v3_chat
      model_name: DeepSeek-V3
      provider: deepseek
      api_base: https://api.deepseek.com/v1
      # api_key 不导出，由导入方自行配置
  prompts:
    - prompt_id: prompt_tsundere_girlfriend_v2
      prompt_name: 傲娇女友人设v2
      system_prompt: |
        你是一个傲娇的女友...
  plugins:
    - plugin_id: plugin_web_search_baidu
      plugin_name: 百度联网搜索
      class_name: WebSearchTool
      plugin_params:
        search_engine: baidu
  memories:
    - memory_id: memory_short_term_10_rounds
      memory_name: 短期记忆-10轮对话
      memory_type: conversation_buffer_window
      memory_params:
        window_size: 10
```

### 1.5 导入校验规则

1. 检查 `export_type` 和 `export_version` 是否匹配
2. 校验必填字段完整性
3. 检查 ID 是否与现有配置冲突（冲突时提供「跳过/覆盖/生成新ID」选项）
4. 敏感字段（api_key）不导入，需用户手动填写
5. 返回导入结果报告（成功/失败/跳过的条目）

### 1.6 技术实现要点

- 使用 `pyyaml` 进行 YAML 序列化/反序列化
- 导出时自动脱敏 `api_key`
- 导入时生成冲突检测报告
- 前端提供文件选择器 + 导入预览 + 冲突处理弹窗

---

## 二、记忆策略完善（P1）

### 2.1 需求背景

文档定义了三种记忆策略，当前仅实现 `conversation_buffer_window`（滑动窗口）

### 2.2 待实现策略

#### 策略 A：对话摘要记忆（conversation_summary）

**原理**：每隔 N 轮对话，调用 LLM 对历史对话进行摘要压缩，保留核心信息

**配置结构**：
```yaml
memory_id: memory_summary_v1
memory_name: 对话摘要记忆
memory_type: conversation_summary
memory_params:
  summary_interval: 10          # 每10轮触发一次摘要
  summary_prompt: "请总结以下对话的核心要点..."  # 可选自定义提示词
  max_summary_length: 500       # 摘要最大长度
  keep_recent: 3                # 保留最近N轮原始对话
```

**实现要点**：
- 使用独立的 LLM 调用进行摘要生成
- 摘要结果存储到 `memory_configs` 表的 `summary_cache` 字段
- 对话时注入：`[历史摘要] + [最近N轮原始对话]`

#### 策略 B：Token 限制记忆（token_buffer）

**原理**：按 Token 数量限制上下文长度，动态裁剪历史消息

**配置结构**：
```yaml
memory_id: memory_token_buffer_v1
memory_name: Token限制记忆-4000
memory_type: token_buffer
memory_params:
  max_tokens: 4000              # 最大Token数
  buffer_ratio: 0.7             # 历史消息占用比例（预留空间给新消息）
  token_estimator: "tiktoken"   # Token计算器：tiktoken / approximate
```

**实现要点**：
- 集成 `tiktoken` 库进行精确 Token 计数
- 从最旧消息开始裁剪，直到总 Token 数低于阈值
- 系统提示词不计入限制

#### 策略 C：长期记忆持久化（跨会话）

**原理**：用户画像、偏好、关键事实跨会话保留

**配置结构**：
```yaml
memory_id: memory_longterm_v1
memory_name: 长期记忆
memory_type: long_term
memory_params:
  extraction_prompt: "从以下对话中提取用户的关键信息..."
  max_facts: 50                 # 最多存储的事实数量
  fact_categories:              # 分类存储
    - preferences               # 偏好
    - personal_info             # 个人信息
    - important_events          # 重要事件
```

**实现要点**：
- 新增 `long_term_memories` 表存储提取的事实
- 每次对话结束后异步提取关键信息
- 对话时按相关性检索并注入上下文

### 2.3 记忆策略切换

- 预设方案的 `selected_memory` 字段引用记忆配置 ID
- 切换预设即自动切换记忆策略
- 前端记忆配置页面提供策略类型选择器

---

## 三、RAG 检索优化（P1）

### 3.1 需求背景

当前 RAG 引擎为基础向量检索，文档要求支持混合检索、重排序、引用展示

### 3.2 待实现功能

#### 功能 A：混合检索（Hybrid Search）

**原理**：结合关键词检索（BM25）和语义检索（向量），提升召回率

**配置结构**：
```yaml
kb_id: kb_python_docs
retrieval_params:
  search_type: hybrid           # hybrid / semantic / keyword
  semantic_weight: 0.7          # 语义检索权重
  keyword_weight: 0.3           # 关键词检索权重
  k: 5                          # 最终返回文档数
  fetch_k: 20                   # 初始召回文档数（用于重排序）
```

**实现要点**：
- ChromaDB 原生支持关键词过滤，可结合 metadata 过滤实现
- 或使用 `rank_bm25` 库实现本地 BM25 检索
- 两路召回结果加权融合后取 Top-K

#### 功能 B：重排序（Rerank）

**原理**：对召回文档进行精细排序，提升 Top 结果相关性

**可选方案**：
| 方案 | 模型 | 部署方式 | 精度 |
|------|------|----------|------|
| BGE M3 | BAAI/bge-m3 | 本地（Ollama/Transformers） | 高 |
| Cohere Rerank | cohere API | 云端 API | 高 |
| ColBERT | colbert-ir | 本地 | 中高 |

**配置结构**：
```yaml
kb_id: kb_python_docs
rerank_config:
  enabled: true
  provider: bge_m3              # bge_m3 / cohere / colbert
  model_name: BAAI/bge-m3
  top_k: 3                      # 重排序后保留的文档数
```

**实现要点**：
- 检索阶段召回 `fetch_k` 个文档
- 重排序阶段对 `(query, doc)` 对打分
- 按分数排序后取 `top_k` 注入上下文

#### 功能 C：检索结果引用展示

**原理**：前端显示 AI 回复引用的知识库文档来源

**实现要点**：
- RAG 引擎返回时附带 `source_documents` 元数据
- 流式输出结束后发送引用信息事件
- 前端渲染为可点击的引用卡片

**API 响应扩展**：
```json
{
  "content": "Python 3.12 引入了...",
  "session_id": "xxx",
  "sources": [
    {
      "doc_id": "doc_001",
      "title": "PEP 695 - 类型参数语法",
      "content_preview": "Python 3.12 引入了新的类型参数语法...",
      "score": 0.92
    }
  ]
}
```

#### 功能 D：文档分块策略优化

**原理**：按文档类型智能分块，避免上下文碎片化

**待实现策略**：
| 策略 | 适用场景 | 说明 |
|------|----------|------|
| 语义分块 | 长文本 | 按语义相似度边界分块 |
| 分层分块 | 结构化文档 | 父块（章节）+ 子块（段落） |
| Markdown 分块 | Markdown 文档 | 按标题层级分块 |
| 固定大小分块 | 通用 | 当前已实现 |

---

## 四、渠道接入完善（P1）

### 4.1 需求背景

文档定义「一套配置·全渠道触达」，当前 OneBot11 适配器骨架已搭建

### 4.2 待实现渠道

#### 渠道 A：OneBot11（QQ 机器人）

**当前状态**：`backend/app/channels/adapters/onebot11.py` 已存在骨架

**待完成**：
- WebSocket 连接管理
- 消息收发完整实现（文本、图片、@提及）
- 事件解析（群消息、私聊、加群事件）
- 预设方案绑定（不同群/用户可绑定不同预设）

**配置结构**：
```yaml
channel_type: onebot11
config:
  ws_url: ws://localhost:6700
  access_token: ""
  bindings:
    - group_id: 123456
      preset_id: preset_github_helper
    - user_id: 789012
      preset_id: preset_girlfriend
```

#### 渠道 B：飞书机器人

**待完成**：
- 飞书开放平台 Webhook 接入
- 事件回调处理
- 消息卡片渲染（支持富文本）
- 预设方案绑定

**配置结构**：
```yaml
channel_type: feishu
config:
  app_id: "cli_xxx"
  app_secret: "xxx"
  verification_token: "xxx"
  bindings:
    - chat_id: "oc_xxx"
      preset_id: preset_feishu_assistant
```

#### 渠道 C：Telegram 机器人

**待完成**：
- Telegram Bot API 接入
- Webhook 或 Long Polling 模式
- Markdown 消息渲染
- 预设方案绑定

**配置结构**：
```yaml
channel_type: telegram
config:
  bot_token: "123456:ABC-DEF"
  bindings:
    - chat_id: "-1001234567890"
      preset_id: preset_telegram_bot
```

### 4.3 渠道服务统一架构

```
channels/
├── adapters/
│   ├── base.py          # 渠道适配器基类
│   ├── onebot11.py      # QQ 机器人
│   ├── feishu.py        # 飞书机器人
│   └── telegram.py      # Telegram 机器人
├── service.py           # 渠道服务（路由、鉴权、消息转换）
└── api/
    └── __init__.py      # 渠道管理 API
```

**适配器基类接口**：
```python
class BaseChannelAdapter(ABC):
    @abstractmethod
    async def send_message(self, channel_id: str, message: str, **kwargs): ...
    
    @abstractmethod
    async def on_message(self, event: Dict) -> Dict: ...
    
    @abstractmethod
    async def start(self): ...
    
    @abstractmethod
    async def stop(self): ...
```

---

## 五、单元测试覆盖（P2）

### 5.1 需求背景

当前无测试文件，核心引擎缺乏自动化验证

### 5.2 测试范围

| 模块 | 测试文件 | 覆盖内容 |
|------|----------|----------|
| 预设引擎 | `tests/test_preset_engine.py` | 预设加载、资源校验、图构建 |
| 插件系统 | `tests/test_plugins.py` | 插件加载、注册表、工具适配 |
| RAG 引擎 | `tests/test_rag_engine.py` | 向量检索、上下文格式化 |
| 工具引擎 | `tests/test_tool_engine.py` | 工具决策、ToolNode 创建 |
| 记忆服务 | `tests/test_memory_service.py` | 历史加载、窗口裁剪 |
| API 接口 | `tests/test_api.py` | CRUD 接口、流式输出 |

### 5.3 测试框架配置

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-asyncio = "^0.23.0"
httpx = "^0.27.0"           # API 测试
pytest-mock = "^3.12.0"     # Mock 支持
```

**conftest.py 核心 fixture**：
```python
@pytest.fixture
async def db_session():
    """测试数据库会话"""
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
def test_client():
    """FastAPI 测试客户端"""
    return TestClient(app)
```

---

## 六、LangSmith 深度集成（P2）

### 6.1 需求背景

当前仅基础追踪接入，未充分利用 LangSmith 能力

### 6.2 待实现功能

| 功能 | 说明 | 实现方式 |
|------|------|----------|
| 提示词版本管理 | Prompt 池每次修改记录版本 | LangSmith Prompt Hub |
| Token 成本统计 | 按预设/模型统计用量 | 自定义回调 + LangSmith API |
| RAG 检索可视化 | 展示查询/召回/重排序过程 | 自定义 trace |
| 用户反馈收集 | 点赞/点踩关联到 Run | `client.create_feedback()` |
| 性能告警 | 慢查询/高错误率告警 | LangSmith 监控面板 |

### 6.3 前端集成

- 对话页面显示「查看 LangSmith 追踪」链接
- 管理页面展示 Token 用量图表
- 反馈按钮关联 LangSmith 评分

---

## 七、性能优化（P2）

### 7.1 需求背景

当前每次对话都重新构建 LangGraph，模型实例有缓存但图无缓存

### 7.2 优化方案

#### 优化 A：Graph 编译缓存

**原理**：相同预设 + 相同配置 → 复用已编译的图

**实现**：
```python
class PresetEngine:
    def __init__(self):
        self._graph_cache: Dict[str, CompiledStateGraph] = {}
    
    async def get_or_build_graph(self, preset: Preset, enable_rag: bool, enable_tools: bool) -> CompiledStateGraph:
        cache_key = f"{preset.preset_id}_rag{enable_rag}_tools{enable_tools}"
        if cache_key not in self._graph_cache:
            self._graph_cache[cache_key] = await self.build_graph(preset, enable_rag, enable_tools)
        return self._graph_cache[cache_key]
```

**失效策略**：
- 预设方案更新时清除对应缓存
- 插件配置变更时清除对应缓存
- 设置 TTL 过期（可选）

#### 优化 B：向量检索缓存

**原理**：相同查询 → 复用检索结果

**实现**：
- 使用 `functools.lru_cache` 或 Redis
- 缓存键：`hash(query + kb_ids + retrieval_params)`
- TTL：5-15 分钟（根据场景调整）

#### 优化 C：异步并发优化

**原理**：RAG 检索和模型调用可并行

**实现**：
```python
# 当前：串行
context = await rag_engine.retrieve(query)
response = await model.ainvoke(prompt + context)

# 优化：并行（如果模型不依赖检索结果）
context_task = rag_engine.retrieve(query)
# ... 其他独立任务
context = await context_task
```

---

## 八、前端功能补全（P2）

### 8.1 待实现功能

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 配置导入导出 UI | 文件选择器 + 预览 + 冲突处理 | P0 |
| 检索结果引用展示 | 回复下方显示来源卡片 | P1 |
| 渠道管理页面 | 渠道配置 + 绑定状态 + 日志 | P1 |
| Token 用量统计 | 图表展示各预设/模型用量 | P2 |
| 提示词版本管理 | 历史版本对比 + 回滚 | P2 |
| 暗黑模式完善 | 部分组件未适配 | P2 |

---

## 九、文档与部署（P2）

### 9.1 待完成文档

| 文档 | 说明 |
|------|------|
| 部署指南 | Docker / 单文件 / 云平台部署步骤 |
| 开发指南 | 本地开发环境搭建、代码规范 |
| 插件开发指南 | 已有 `docs/plugin_system.md`，需补充示例 |
| API 文档 | 自动生成 Swagger，需补充使用示例 |
| 常见问题 FAQ | 部署报错、模型配置、渠道接入等 |

### 9.2 部署配置

| 配置 | 说明 |
|------|------|
| Dockerfile | 多阶段构建，分离前端/后端 |
| docker-compose.yml | 一键启动后端 + 前端 |
| .env.example | 环境变量模板 |
| Railway/Fly.io 配置 | 云平台部署配置文件 |

---

## 优先级总结

| 优先级 | 模块 | 预估工作量 | 核心价值 |
|--------|------|------------|----------|
| P0 | 配置文件导入导出 | 2-3 小时 | 核心卖点闭环 |
| P1 | 记忆策略完善 | 2-3 小时 | 长对话场景支持 |
| P1 | RAG 检索优化 | 3-4 小时 | 知识库准确率提升 |
| P1 | 渠道接入完善 | 4-6 小时 | 全渠道触达 |
| P2 | 单元测试覆盖 | 3-4 小时 | 迭代质量保障 |
| P2 | LangSmith 深度集成 | 1-2 小时 | 生产级调试 |
| P2 | 性能优化 | 2-3 小时 | 响应速度提升 |
| P2 | 前端功能补全 | 4-6 小时 | 用户体验提升 |
| P2 | 文档与部署 | 2-3 小时 | 降低使用门槛 |

---

> 注：以上工作量为独立开发预估，部分模块可并行推进。
> 建议按 P0 → P1 → P2 顺序迭代，每个优先级完成后进行一次发布。
