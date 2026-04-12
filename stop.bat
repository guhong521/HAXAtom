@echo off
chcp 65001 >nul 2>&1
title HAXAtom - 停止服务

echo.
echo ============================================================
echo   HAXAtom 服务停止器
echo ============================================================
echo.

echo [1/2] 停止后端服务 (uvicorn)...
taskkill /fi "WINDOWTITLE eq HAXAtom-Backend*" /f >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    taskkill /pid %%a /f >nul 2>&1
)
echo [OK] 后端服务已停止

echo [2/2] 停止前端服务 (vite)...
taskkill /fi "WINDOWTITLE eq HAXAtom-Frontend*" /f >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5173" ^| findstr "LISTENING"') do (
    taskkill /pid %%a /f >nul 2>&1
)
echo [OK] 前端服务已停止

echo.
echo ============================================================
echo   所有服务已停止
echo ============================================================
echo.

pause
