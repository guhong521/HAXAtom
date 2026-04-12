# HAXAtom 快速启动指南

## 快速启动

### Windows PowerShell（推荐）

**启动项目：**
```powershell
.\start.ps1
```

**停止项目：**
```powershell
.\stop.ps1
```

### Windows CMD

**启动项目：**
```cmd
start.bat
```

**停止项目：**
```cmd
stop.bat
```

## 脚本功能

### start.ps1 / start.bat

1. 自动检查 Python 环境
2. 自动检查 Poetry（可选）
3. 自动检查 Node.js 和 npm
4. 自动安装前端依赖（如未安装）
5. 启动后端服务（http://localhost:8000）
6. 启动前端服务（http://localhost:5173）
7. 自动打开浏览器

### stop.ps1 / stop.bat

1. 停止后端 uvicorn 服务（端口 8000）
2. 停止前端 vite 服务（端口 5173）

## 访问地址

- **前端界面**: http://localhost:5173
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

## 注意事项

1. 关闭启动脚本窗口**不会**停止服务
2. 需要停止服务时，请运行 `stop.ps1` 或 `stop.bat`
3. 也可以手动关闭启动的两个 CMD 窗口来停止服务

## 环境要求

- Python 3.11+
- Node.js 18+
- Poetry（可选，用于后端依赖管理）
