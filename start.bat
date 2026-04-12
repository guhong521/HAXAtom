@echo off
title HAXAtom - One Click Start

echo.
echo ============================================================
echo   HAXAtom Quick Start
echo ============================================================
echo.

:: ============ Check Backend Environment ============
echo [1/4] Checking backend environment...

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python not found. Please install Python 3.11+
    pause
    exit /b 1
)
echo [OK] Python found

where poetry >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Poetry not found, using pip mode
    set USE_POETRY=0
) else (
    echo [OK] Poetry found
    set USE_POETRY=1
)

:: ============ Check Frontend Environment ============
echo [2/4] Checking frontend environment...

where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)
echo [OK] Node.js found

where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] npm not found
    pause
    exit /b 1
)
echo [OK] npm found

if not exist "frontend\node_modules" (
    echo [!] Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
    if %errorlevel% neq 0 (
        echo [X] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
)

:: ============ Start Backend ============
echo [3/4] Starting backend service...
echo       URL: http://localhost:8000
echo       API: http://localhost:8000/docs

if "%USE_POETRY%"=="1" (
    start "HAXAtom-Backend" cmd /k "cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
) else (
    start "HAXAtom-Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
)

timeout /t 3 /nobreak >nul

:: ============ Start Frontend ============
echo [4/4] Starting frontend service...
echo       URL: http://localhost:5173

start "HAXAtom-Frontend" cmd /k "cd frontend && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ============================================================
echo   STARTED!
echo.
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo   Close this window does NOT stop services
echo   Run stop.bat to stop all services
echo ============================================================
echo.

echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:5173

pause
