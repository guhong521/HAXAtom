# HAXAtom

<div align="center">

**「原子化解耦 · 乐高式拼装」的全栈 AI 智能体管理与多端分发平台**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/vue-3.4+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/langchain-0.3+-green.svg)](https://python.langchain.com/)

**一套配置，全端触达，无限自定义的 AI 智能体中枢**

</div>

---

## 🌟 项目简介

HAXAtom 是一款基于 **LangChain + LangGraph** 构建的全栈 AI 智能体（Agent）管理与多端分发平台。采用「**原子化解耦配置**」为核心设计理念，原生集成 Web 全功能控制台、企业级 RAG 知识库、可视化 Agent 编排能力，兼顾小白用户的开箱即用与开发者的高自由度自定义。

### 核心设计思想

- 🔗 **彻底解耦** - 模型、提示词、插件、知识库、记忆五大模块完全独立
- 🧩 **池化复用** - 五大资源池一次配置，全项目无限复用
- 🎯 **乐高拼装** - 预设方案从资源池挑选零件，快速组装 AI 智能体
- 🚀 **轻量部署** - 支持单 exe/Docker 一键启动，无需复杂中间件
- 🌐 **全渠道触达** - 一套配置同时支持 Web、飞书、钉钉、QQ、Telegram

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│              交互层 (Interaction Layer)                  │
│  Web 管理端 │ Web 对话端 │ 飞书/钉钉/QQ/Telegram          │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│            路由适配层 (Routing Layer)                    │
│     统一消息封装 │ 鉴权限流 │ 全局异常拦截 │ 多渠道适配   │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│            核心引擎层 (Core Engine)                      │
│  预设组合引擎 │ LangGraph 工作流 │ RAG 检索 │ 工具调用   │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│           资源池层 (Resource Pools)                      │
│    模型池 │ 提示词池 │ 插件池 │ 知识库池 │ 记忆池       │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│             存储层 (Storage Layer)                       │
│      SQLite │ ChromaDB │ 本地文件系统                    │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ 核心特性

### 🎨 五大原子化资源池

| 资源池 | 功能描述 | 复用性 |
|--------|---------|--------|
| **模型池** | 管理所有大模型配置（OpenAI、智谱、DeepSeek 等） | 一次配置，全预设复用 |
| **提示词池** | 管理人设、系统提示词配置 | 无限次复用 |
| **插件池** | 管理工具插件（搜索、天气、计算器等） | 热插拔复用 |
| **知识库池** | 管理企业级 RAG 知识库 | 多预设共享 |
| **记忆池** | 管理对话记忆策略 | 灵活配置 |

### 🧩 预设方案（Preset）

像搭乐高一样拼装 AI 智能体：

```yaml
preset_id: preset_tsundere_girlfriend_deepseek
preset_name: 傲娇女友（DeepSeek-V3）
selected_model: model_deepseek_v3_chat        # 引用模型池
selected_prompt: prompt_tsundere_girlfriend_v2 # 引用提示词池
selected_plugins:                               # 引用插件池
  - plugin_web_search_baidu
  - plugin_weather_query
selected_knowledge_bases:                      # 引用知识库池
  - kb_our_chat_history
selected_memory: memory_short_term_10_rounds   # 引用记忆池
```

### 🚀 技术栈选型

| 维度 | 技术选型 | 说明 |
|------|---------|------|
| **前端框架** | Vue 3 + Vite + Tailwind CSS | Composition API + 响应式 UI |
| **UI 组件** | Element Plus + Lucide Icons | 企业级组件库 |
| **后端框架** | Python 3.11+ + FastAPI | 全异步高性能 API |
| **AI 核心** | LangChain Core + LCEL + LangGraph | 最新稳定版，拒绝废弃 API |
| **可观测性** | LangSmith | 全链路追踪 + Token 统计 |
| **数据库** | SQLite + ChromaDB | 轻量级嵌入式存储 |
| **部署方式** | PyInstaller / Docker | 单 exe / 容器化一键部署 |

---

## 🎯 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- Git

### 1. 克隆项目

```bash
git clone https://github.com/guhong521/HAXAtom.git
cd HAXAtom
```

### 2. 安装后端依赖

```bash
cd backend
pip install poetry
poetry install
```

### 3. 安装前端依赖

```bash
cd frontend
npm install
```

### 4. 启动开发服务

**后端：**
```bash
cd backend
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**前端：**
```bash
cd frontend
npm run dev
```

### 5. 访问控制台

打开浏览器访问：`http://localhost:5173`

---

## 📦 部署方案

### Windows 单 exe 文件（推荐）

```bash
# 打包为单个可执行文件
pyinstaller --onefile --add-data "frontend/dist:frontend/dist" backend/app/main.py
```

**优势：** 双击即可运行，无需安装 Python 环境

### Docker 一键部署

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f
```

**优势：** 支持 Linux 服务器、NAS 等环境，数据持久化

---

## 🛠️ 开发指南

### 项目结构

```
HAXAtom/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API 路由
│   │   ├── core/              # 核心引擎
│   │   ├── db/                # 数据库管理
│   │   ├── models/            # 数据模型
│   │   ├── schemas/           # Pydantic 模型
│   │   └── utils/             # 工具函数
│   └── poetry.lock
├── frontend/                   # 前端项目
│   ├── src/
│   │   ├── api/               # API 调用
│   │   ├── components/        # 组件
│   │   ├── locales/           # 国际化
│   │   ├── router/            # 路由配置
│   │   ├── stores/            # Pinia 状态管理
│   │   ├── views/             # 页面视图
│   │   └── App.vue
│   └── package.json
├── docs/                       # 文档
└── README.md
```

### 添加新模型提供商

1. 在 `backend/app/models/model_config.py` 添加模型配置
2. 在 `frontend/src/views/bot/pages/ModelProviderView.vue` 添加 UI
3. 更新国际化文件

### 开发新插件

1. 继承 `BaseTool` 类实现工具逻辑
2. 在插件池配置中注册
3. 预设方案中引用即可使用

---

## 🔒 安全规范

- ✅ 所有管理接口 JWT 鉴权
- ✅ 敏感配置（API Key）加密存储
- ✅ 频率限制防止刷接口
- ✅ 支持 HTTPS 配置
- ✅ 一键备份与恢复功能

---

## 📄 文档

- [系统架构文档](架构.md) - 详细的架构设计说明
- [开发文档](docs/) - 开发指南与 API 文档
- [部署文档](docs/deployment.md) - 部署教程

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📝 更新日志

### v0.1.0 (2025)
- ✨ 初始版本发布
- 🎨 五大资源池管理功能
- 🧩 预设方案编辑器
- 💬 Web 对话端
- 📚 RAG 知识库集成
- 🔌 插件系统

---

## 👨‍💻 作者

- **guhong521** - [GitHub](https://github.com/guhong521)

---

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 🙏 致谢

感谢以下开源项目：

- [Vue.js](https://vuejs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://python.langchain.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Element Plus](https://element-plus.org/)
- [Tailwind CSS](https://tailwindcss.com/)

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star 支持！**

</div>
