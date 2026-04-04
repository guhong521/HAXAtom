# HAXAtom Backend

HAXAtom 后端服务 - 一款「原子化解耦、乐高式拼装」的全栈AI智能体管理与多端分发平台。

## 技术栈

- **Web框架**: FastAPI + Uvicorn
- **AI框架**: LangChain Core + LCEL + LangGraph
- **数据库**: SQLite + SQLAlchemy 2.0 (异步)
- **向量存储**: ChromaDB
- **可观测性**: LangSmith

## 快速开始

### 1. 安装依赖

```bash
# 使用 Poetry
poetry install

# 或使用 pip
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件配置你的参数
```

### 3. 初始化数据库

```bash
alembic upgrade head
```

### 4. 启动服务

```bash
# 开发模式
poetry run uvicorn app.main:app --reload

# 生产模式
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 项目结构

```
app/
├── api/          # API路由
├── core/         # 核心引擎
├── db/           # 数据库配置
├── models/       # SQLAlchemy模型
├── schemas/      # Pydantic Schema
├── services/     # 业务逻辑
├── plugins/      # 插件系统
├── vectorstore/  # 向量存储
└── utils/        # 工具函数
```

## API文档

启动服务后访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
