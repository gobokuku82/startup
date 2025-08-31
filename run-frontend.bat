@echo off
REM Frontend Execution Script

echo ========================================
echo   Frontend Server - React + Vite
echo ========================================
echo.

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed.
    echo Please install Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

REM Save current directory
set ROOT_DIR=%CD%

REM Change to frontend directory
cd /d "%ROOT_DIR%\frontend"

REM Check node_modules
if not exist "node_modules" (
    echo [INFO] Installing packages... (first run takes 5-10 minutes)
    call npm install
    echo [OK] Packages installed
)

echo.
echo ========================================
echo   Starting Frontend Server
echo   URL: http://localhost:3000
echo   Stop: Ctrl+C
echo ========================================
echo.

REM Start development server
call npm run dev

REM Return to root directory
cd /d "%ROOT_DIR%"

pause