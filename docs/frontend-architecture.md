# HAXAtom 前端架构设计文档

## 一、技术栈选型

| 技术 | 版本/说明 | 选型理由 |
|------|----------|----------|
| **框架** | Vue 3.4+ | Composition API 易维护，性能优秀 |
| **构建工具** | Vite 5+ | 极速热更新，构建速度快 |
| **样式** | Tailwind CSS 3.4+ | 原子化CSS，快速开发响应式UI |
| **UI组件库** | Element Plus 2.5+ | 成熟企业级组件库，功能完善 |
| **图标** | Lucide Vue | 现代化图标库，轻量美观 |
| **状态管理** | Pinia 2.1+ | Vue官方推荐，TypeScript友好 |
| **路由** | Vue Router 4+ | 官方路由，支持动态路由 |
| **HTTP客户端** | Axios 1.6+ | 成熟稳定，拦截器机制完善 |
| **Markdown渲染** | marked 9+ | 轻量级Markdown解析 |
| **代码高亮** | highlight.js 11+ | 支持多种编程语言高亮 |

## 二、项目目录结构

```
frontend/
├── public/                    # 静态资源
│   └── favicon.ico
├── src/
│   ├── api/                   # API接口封装
│   │   ├── index.ts           # 统一导出
│   │   ├── models.ts          # 模型配置API
│   │   ├── prompts.ts         # 提示词配置API
│   │   ├── plugins.ts         # 插件配置API
│   │   ├── knowledge.ts       # 知识库API
│   │   ├── memories.ts        # 记忆配置API
│   │   ├── presets.ts         # 预设方案API
│   │   └── chat.ts            # 对话API
│   │
│   ├── components/            # 公共组件
│   │   ├── common/            # 通用组件
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppSidebar.vue
│   │   │   ├── DataTable.vue
│   │   │   └── FormDialog.vue
│   │   ├── chat/              # 对话相关组件
│   │   │   ├── ChatMessage.vue
│   │   │   ├── ChatInput.vue
│   │   │   ├── ChatSidebar.vue
│   │   │   └── MarkdownRenderer.vue
│   │   └── preset/            # 预设方案组件
│   │       ├── PresetSelector.vue
│   │       └── ResourceBadge.vue
│   │
│   ├── views/                 # 页面视图
│   │   ├── layout/            # 布局组件
│   │   │   ├── MainLayout.vue # 主布局（侧边栏+内容区）
│   │   │   └── ChatLayout.vue # 对话布局
│   │   ├── bot/               # Bot管理端视图
│   │   │   ├── Dashboard.vue
│   │   │   ├── ModelManager.vue
│   │   │   ├── PromptManager.vue
│   │   │   ├── PluginManager.vue
│   │   │   ├── KnowledgeManager.vue
│   │   │   ├── MemoryManager.vue
│   │   │   └── PresetManager.vue
│   │   ├── chat/              # Chat对话端视图
│   │   │   └── ChatView.vue
│   │   └── system/            # 系统管理视图
│   │       └── Settings.vue
│   │
│   ├── stores/                # Pinia状态管理
│   │   ├── index.ts
│   │   ├── app.ts             # 应用状态
│   │   ├── preset.ts          # 预设方案状态
│   │   ├── chat.ts            # 对话状态
│   │   └── user.ts            # 用户状态
│   │
│   ├── router/                # 路由配置
│   │   └── index.ts
│   │
│   ├── utils/                 # 工具函数
│   │   ├── request.ts         # Axios封装
│   │   ├── sse.ts             # SSE流式处理
│   │   ├── format.ts          # 格式化工具
│   │   └── storage.ts         # 本地存储
│   │
│   ├── types/                 # TypeScript类型定义
│   │   ├── model.ts
│   │   ├── preset.ts
│   │   ├── chat.ts
│   │   └── common.ts
│   │
│   ├── styles/                # 样式文件
│   │   ├── index.css          # 入口样式
│   │   ├── element-plus.css   # Element Plus覆盖
│   │   └── markdown.css       # Markdown样式
│   │
│   ├── App.vue                # 根组件
│   ├── main.ts                # 入口文件
│   └── env.d.ts               # 环境类型声明
│
├── index.html                 # HTML模板
├── package.json               # 依赖配置
├── tsconfig.json              # TypeScript配置
├── vite.config.ts             # Vite配置
├── tailwind.config.js         # Tailwind配置
└── .env                       # 环境变量
```

## 三、核心功能模块设计

### 3.1 Bot视图（管理端）

**功能定位**：五大资源池与预设方案的可视化编辑器

**页面清单**：
- **Dashboard** - 系统概览，统计信息
- **ModelManager** - 模型配置管理（增删改查、导入导出）
- **PromptManager** - 提示词配置管理
- **PluginManager** - 插件配置管理
- **KnowledgeManager** - 知识库管理（文档上传、向量化）
- **MemoryManager** - 记忆配置管理
- **PresetManager** - 预设方案拼装器（核心页面）

**PresetManager 核心交互**：
```
┌─────────────────────────────────────────────────────────┐
│ 预设方案编辑器                                              │
├─────────────────────────────────────────────────────────┤
│ 预设名称: [________]  预设ID: [________]                  │
│ 描述: [________]                                         │
├─────────────────────────────────────────────────────────┤
│ 选择聊天模型    [▼ 下拉选择模型池中的模型]                 │
│ 选择人设提示词  [▼ 下拉选择提示词池中的提示词]             │
│ 选择知识库      [☑ 多选框选择知识库池中的知识库]           │
│ 选择插件        [☑ 多选框选择插件池中的插件]               │
│ 选择记忆策略    [▼ 下拉选择记忆池中的配置]                 │
├─────────────────────────────────────────────────────────┤
│ [保存预设]  [导出YAML]  [测试对话]                        │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Chat视图（对话端）

**功能定位**：预设方案的使用者，沉浸式对话体验

**核心组件**：
- **PresetSelector** - 顶部预设方案切换器
- **ChatSidebar** - 左侧对话历史列表
- **ChatMessage** - 消息气泡组件（支持Markdown）
- **ChatInput** - 底部输入框（支持快捷操作）

**界面布局**：
```
┌─────────────────────────────────────────────────────────┐
│ [Logo]  HAXAtom    [▼ 预设方案选择器]    [设置] [导出]   │
├──────────┬──────────────────────────────────────────────┤
│          │                                              │
│ 对话历史  │           对话消息区域                        │
│          │                                              │
│ • 对话1  │  ┌─────────────────────────────┐             │
│ • 对话2  │  │ 用户: 你好                  │             │
│ • 对话3  │  └─────────────────────────────┘             │
│          │  ┌─────────────────────────────┐             │
│ [新建]   │  │ AI: 你好！有什么可以帮助你？│             │
│          │  └─────────────────────────────┘             │
│          │                                              │
├──────────┴──────────────────────────────────────────────┤
│ [📎] [输入框...                    ] [发送]             │
└─────────────────────────────────────────────────────────┘
```

## 四、状态管理设计

### 4.1 Store划分

```typescript
// stores/app.ts - 应用级状态
interface AppState {
  sidebarCollapsed: boolean    // 侧边栏折叠状态
  theme: 'light' | 'dark'      // 主题
  loading: boolean             // 全局加载状态
}

// stores/preset.ts - 预设方案状态
interface PresetState {
  presets: Preset[]            // 预设方案列表
  currentPreset: Preset | null // 当前选中的预设
  resources: {                 // 五大资源池缓存
    models: ModelConfig[]
    prompts: PromptConfig[]
    plugins: PluginConfig[]
    knowledgeBases: KnowledgeBase[]
    memories: MemoryConfig[]
  }
}

// stores/chat.ts - 对话状态
interface ChatState {
  conversations: Conversation[]  // 对话列表
  currentSessionId: string | null // 当前会话ID
  messages: Message[]            // 当前对话消息
  streaming: boolean             // 是否正在流式输出
}
```

## 五、API封装设计

### 5.1 统一响应格式

```typescript
// types/common.ts
interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

// 统一错误处理
interface ApiError {
  code: number
  message: string
  detail?: string
}
```

### 5.2 API模块划分

```typescript
// api/models.ts
export const modelApi = {
  getList: () => request.get<ApiResponse<ModelConfig[]>>('/models'),
  create: (data: ModelConfigCreate) => request.post<ApiResponse<ModelConfig>>('/models', data),
  update: (id: string, data: ModelConfigUpdate) => request.patch<ApiResponse<ModelConfig>>(`/models/${id}`, data),
  delete: (id: string) => request.delete<ApiResponse<void>>(`/models/${id}`),
}

// api/chat.ts - 包含SSE流式处理
export const chatApi = {
  sendMessage: (data: ChatRequest) => request.post<ApiResponse<ChatResponse>>('/chat/completions', data),
  sendMessageStream: (data: ChatRequest) => {
    // 返回EventSource对象
    return new EventSource(`/api/v1/chat/completions/stream?...`)
  }
}
```

## 六、路由设计

```typescript
// router/index.ts
const routes = [
  {
    path: '/',
    component: MainLayout,
    redirect: '/chat',
    children: [
      // Bot管理端
      { path: '/bot', component: Dashboard, meta: { title: '控制台' } },
      { path: '/bot/models', component: ModelManager, meta: { title: '模型管理' } },
      { path: '/bot/prompts', component: PromptManager, meta: { title: '提示词管理' } },
      { path: '/bot/plugins', component: PluginManager, meta: { title: '插件管理' } },
      { path: '/bot/knowledge', component: KnowledgeManager, meta: { title: '知识库' } },
      { path: '/bot/memories', component: MemoryManager, meta: { title: '记忆管理' } },
      { path: '/bot/presets', component: PresetManager, meta: { title: '预设方案' } },
      
      // Chat对话端
      { path: '/chat', component: ChatView, meta: { title: '对话' } },
      { path: '/chat/:sessionId', component: ChatView, meta: { title: '对话' } },
      
      // 系统管理
      { path: '/system/settings', component: Settings, meta: { title: '系统设置' } },
    ]
  }
]
```

## 七、开发顺序

1. **Phase 1: 基础骨架** (1-2天)
   - Vite + Vue3 + TypeScript 项目初始化
   - 配置 Tailwind CSS + Element Plus
   - 搭建路由和布局框架
   - 配置 Axios 和 Pinia

2. **Phase 2: API对接** (1天)
   - 封装所有后端API
   - 定义TypeScript类型
   - 实现请求拦截器和错误处理

3. **Phase 3: 对话功能** (2-3天)
   - ChatView 页面开发
   - 消息组件（支持Markdown）
   - SSE流式输出实现
   - 预设方案切换器

4. **Phase 4: 管理功能** (3-4天)
   - 五大资源池管理页面
   - 预设方案拼装器
   - 数据表格和表单组件

5. **Phase 5: 优化完善** (2天)
   - UI细节优化
   - 响应式适配
   - 主题切换

## 八、环境变量配置

```bash
# .env.development
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=HAXAtom
VITE_APP_VERSION=0.1.0

# .env.production
VITE_API_BASE_URL=/api/v1
VITE_APP_TITLE=HAXAtom
VITE_APP_VERSION=0.1.0
```

---

**文档版本**: v1.0  
**创建日期**: 2026-04-01  
**作者**: HAXAtom Team
