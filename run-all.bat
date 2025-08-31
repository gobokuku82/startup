@echo off
REM Backend + Frontend Full Stack Execution

echo ========================================
echo   Startup Manager - Full Stack
echo   Backend + Frontend
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed.
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed.
    pause
    exit /b 1
)

echo [INFO] Starting servers in separate windows...
echo.

REM Get current directory
set PROJECT_DIR=%CD%

REM Start Backend (new window)
start "Backend Server" cmd /c "cd /d %PROJECT_DIR% && call run.bat"

REM Wait 3 seconds
timeout /t 3 /nobreak >nul

REM Start Frontend (new window)
start "Frontend Server" cmd /c "cd /d %PROJECT_DIR% && call run-frontend.bat"

echo.
echo ========================================
echo   Servers Started!
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:3000
echo   API Docs: http://localhost:8000/api/docs
echo ========================================
echo.
echo Two new windows are running the servers.
echo Press Ctrl+C in each window to stop.
echo.

pause