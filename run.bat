@echo off
REM Startup Manager - Windows Execution Script

echo ========================================
echo   Startup Manager - AI Platform
echo   LangGraph 0.6.6 + FastAPI
echo ========================================
echo.

REM Check Python version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed.
    echo Please install Python 3.11 or higher.
    pause
    exit /b 1
)

REM Check virtual environment
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check package installation
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing packages... (this may take a while)
    pip install -r requirements.txt
    echo [OK] Packages installed
)

REM Check .env file
if not exist ".env" (
    echo [INFO] Creating .env file...
    copy .env.example .env >nul
    echo [WARNING] Please edit .env file and set OPENAI_API_KEY!
    echo.
    pause
)

REM Create database directory
if not exist "data\sqlite" (
    echo [INFO] Creating data directory...
    mkdir data\sqlite
)

REM Check database
if not exist "data\sqlite\startup.db" (
    echo [INFO] Initializing database...
    python backend\app\db\init_db.py
    echo [OK] Database initialized
)

echo.
echo ========================================
echo   Starting Server
echo   URL: http://localhost:8000
echo   API Docs: http://localhost:8000/api/docs
echo   Stop: Ctrl+C
echo ========================================
echo.

REM Start server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

pause