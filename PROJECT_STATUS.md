# HAXAtom 项目开发进度

> 最后更新：2026-04-01

## 项目概述

HAXAtom 是一款「原子化解耦、乐高式拼装」的全栈AI智能体管理与多端分发平台。

### 核心设计理念

- **原子化解耦**：模型、提示词、插件、知识库、记忆五大资源独立配置
- **乐高式拼装**：通过预设方案(Preset)灵活组合原子化资源
- **一次配置，多端分发**：Web、飞书、钉钉、Telegram等渠道共享同一配置

---

## 已完成内容

### 1. 项目架构搭建 ✅

```
HAXAtom/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/     # API路由
│   │   │   ├── chat.py           # 对话接口
│   │   │   ├── model_configs.py  # 模型配置管理
│   │   │   ├── presets.py        # 预设方案管理
│   │   │   └── prompt_configs.py # 提示词配置管理
│   │   ├── core/
│   │   │   └── preset_engine.py  # 核心引擎
│   │   ├── db/
│   │   │   ├── migrations/       # Alembic迁移
│   │   │   ├── session.py        # 数据库会话
│   │   │   └── __init__.py
│   │   ├── models/               # SQLAlchemy模型
│   │   │   ├── base.py           # 基础模型
│   │   │   ├── model_config.py   # 模型配置表
│   │   │   ├── prompt_config.py  # 提示词配置表
│   │   │   ├── plugin_config.py  # 插件配置表
│   │   │   ├── knowledge_base.py # 知识库配置表
│   │   │   ├── memory_config.py  # 记忆配置表
│   │   │   ├── preset.py         # 预设方案表
│   │   │   └── conversation.py   # 对话历史表
│   │   ├── schemas/              # Pydantic Schema
│   │   │   ├── common.py         # 通用响应模型
│   │   │   ├── model_config.py   # 模型配置Schema
│   │   │   ├── prompt_config.py  # 提示词配置Schema
│   │   │   ├── preset.py         # 预设方案Schema
│   │   │   └── chat.py           # 对话相关Schema
│   │   ├── config.py             # 应用配置
│   │   └── main.py               # FastAPI主应用
│   ├── pyproject.toml            # Poetry依赖配置
│   ├── alembic.ini               # Alembic配置
│   └── README.md
└── data/                         # 数据目录
    ├── db/                       # SQLite数据库
    ├── vectorstore/              # ChromaDB向量存储
    └── uploads/                  # 文件上传目录
```

### 2. 技术栈 ✅

| 层级 | 技术选型 | 版本 |
|------|----------|------|
| **Web框架** | FastAPI | ^0.115.0 |
| **AI框架** | LangChain Core + LCEL + LangGraph | ^0.3.0 / ^0.2.0 |
| **数据库** | SQLite + SQLAlchemy 2.0 (异步) | ^2.0.35 |
| **向量存储** | ChromaDB | ^0.5.0 |
| **可观测性** | LangSmith | ^0.1.0 |
| **部署** | Uvicorn + Docker | - |

### 3. 数据库设计 ✅

#### 五大资源池表

| 表名 | 说明 | 核心字段 |
|------|------|----------|
| `model_configs` | 模型配置池 | model_id, provider, api_base, api_key |
| `prompt_configs` | 提示词配置池 | prompt_id, system_prompt, variables |
| `plugin_configs` | 插件配置池 | plugin_id, class_name, module_path |
| `knowledge_bases` | 知识库配置池 | kb_id, collection_name, embedding_model |
| `memory_configs` | 记忆配置池 | memory_id, memory_type, memory_params |

#### 核心载体表

| 表名 | 说明 | 核心字段 |
|------|------|----------|
| `presets` | 预设方案 | 引用五大资源池ID |
| `conversations` | 对话历史 | session_id, preset_id, messages(JSON) |

### 4. API 接口 ✅

#### 健康检查
- `GET /` - 根路由
- `GET /health` - 健康检查
- `GET /docs` - Swagger UI 文档
- `GET /redoc` - ReDoc 文档

#### 模型配置管理
- `GET /api/v1/models` - 获取模型列表
- `GET /api/v1/models/{model_id}` - 获取模型详情
- `POST /api/v1/models` - 创建模型配置
- `PUT /api/v1/models/{model_id}` - 更新模型配置
- `DELETE /api/v1/models/{model_id}` - 删除模型配置

#### 提示词配置管理
- `GET /api/v1/prompts` - 获取提示词列表
- `GET /api/v1/prompts/{prompt_id}` - 获取提示词详情
- `POST /api/v1/prompts` - 创建提示词配置
- `PUT /api/v1/prompts/{prompt_id}` - 更新提示词配置
- `DELETE /api/v1/prompts/{prompt_id}` - 删除提示词配置

#### 预设方案管理
- `GET /api/v1/presets` - 获取预设方案列表
- `GET /api/v1/presets/{preset_id}` - 获取预设方案详情
- `POST /api/v1/presets` - 创建预设方案
- `PUT /api/v1/presets/{preset_id}` - 更新预设方案
- `DELETE /api/v1/presets/{preset_id}` - 删除预设方案
- `POST /api/v1/presets/{preset_id}/clone` - 克隆预设方案

#### 对话接口
- `POST /api/v1/chat/completions` - 对话补全（非流式）
- `POST /api/v1/chat/completions/stream` - 对话补全（SSE流式）

### 5. 核心引擎 (PresetEngine) ✅

**功能**：
- 根据 preset_id 加载预设方案
- 从五大资源池获取原子化配置
- 动态组装 LangChain 链
- 支持多种模型提供商（OpenAI、DeepSeek、Ollama、Anthropic）
- 支持流式和非流式输出
- 模型实例缓存优化

### 6. 环境配置 ✅

- Python 3.11+ 虚拟环境
- Poetry 依赖管理
- 所有依赖安装完成
- 服务可正常启动

---

## 启动方式

### 开发模式

```bash
cd f:\2025python\HAXAtom\backend
.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 生产模式

```bash
cd f:\2025python\HAXAtom\backend
.venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 访问地址

- 应用根目录：http://127.0.0.1:8000/
- API文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/health

---

## 下一步开发建议

### 优先级：高

#### 1. 初始化数据脚本
- 创建默认模型配置（如 OpenAI GPT-4、DeepSeek V3、Ollama llama3）
- 创建默认提示词模板
- 创建示例预设方案

#### 2. 对话历史管理完善
- 实现对话历史的持久化存储
- 添加对话列表查询接口
- 实现对话标题自动生成
- 添加对话删除、清空功能

#### 3. 插件系统框架
- 定义 BasePlugin 基类
- 实现插件加载器
- 创建示例插件（如天气查询、计算器）
- 集成到 PresetEngine 中

### 优先级：中

#### 4. 知识库功能
- 集成 ChromaDB 客户端
- 实现文档上传接口（PDF、TXT、MD）
- 实现文档分块和向量化
- 在 PresetEngine 中集成 RAG 检索

#### 5. 记忆系统
- 实现短期记忆（对话窗口）
- 实现长期记忆（摘要存储）
- 集成到对话流程中

#### 6. 前端界面
- 使用 Vue3 + TypeScript 创建管理界面
- 实现模型配置管理页面
- 实现提示词配置管理页面
- 实现预设方案管理页面
- 实现对话界面（支持流式输出）

### 优先级：低

#### 7. 渠道适配器
- 实现飞书机器人适配器
- 实现钉钉机器人适配器
- 实现 Telegram Bot 适配器
- 统一消息格式转换

#### 8. 高级功能
- 多智能体编排（LangGraph）
- 工作流可视化编辑器
- 提示词版本管理
- A/B 测试支持

#### 9. 部署优化
- Dockerfile 编写
- docker-compose.yml 配置
- PyInstaller 打包脚本
- 系统服务配置（systemd）

#### 10. 测试与文档
- 单元测试（pytest）
- API 集成测试
- 完整的使用文档
- 部署指南

---

## 注意事项

### Windows 环境
- 已处理控制台 UTF-8 编码问题
- 使用 `chroma-hnswlib==0.7.5` 避免编译问题

### 数据库
- 使用 SQLite + aiosqlite 异步驱动
- 数据库文件位于 `data/db/haxatom.db`
- 自动创建表结构（无需手动迁移）

### API 密钥安全
- API 密钥存储在数据库中（建议后续加密）
- 响应中 API 密钥显示为 `***SET***`
- 生产环境应使用环境变量或密钥管理服务

---

## 项目文档

- [README.md](./backend/README.md) - 后端服务说明
- [IMPLEMENTATION.md](./IMPLEMENTATION.md) - 详细实现方案
- [PROJECT_STATUS.md](./PROJECT_STATUS.md) - 本文件，开发进度跟踪
