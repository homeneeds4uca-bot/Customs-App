@echo off
REM CustomsCompass Windows Setup Script
REM Run this from PowerShell or Command Prompt as Administrator

echo.
echo ========================================
echo  CustomsCompass Windows Setup
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Please run this script as Administrator
    echo Right-click and select "Run as Administrator"
    pause
    exit /b 1
)

echo Checking prerequisites...
echo.

REM Check Docker
docker --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [X] Docker not found
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
) else (
    echo [OK] Docker installed
)

REM Check Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [X] Python not found
    echo Please install Python 3.11+ from: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo [OK] Python installed
)

REM Check Node.js
node --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [X] Node.js not found
    echo Please install Node.js 18+ from: https://nodejs.org/
    pause
    exit /b 1
) else (
    echo [OK] Node.js installed
)

REM Check npm
npm --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [X] npm not found
    pause
    exit /b 1
) else (
    echo [OK] npm installed
)

echo.
echo All prerequisites met!
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo [OK] Created .env file
    echo.
    echo IMPORTANT: Please update .env with your SECRET_KEY
    echo Generate one with PowerShell:
    echo   -join ((48..57) + (65..90) + (97..122) ^| Get-Random -Count 64 ^| ForEach-Object {[char]$_})
    echo.
    pause
)

echo.
echo ========================================
echo  Starting Docker Services
echo ========================================
echo.

docker compose up -d

if %errorLevel% neq 0 (
    echo [X] Failed to start Docker services
    echo Make sure Docker Desktop is running
    pause
    exit /b 1
)

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
docker compose ps
echo.

echo.
echo ========================================
echo  Setting up Backend
echo ========================================
echo.

cd backend

if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

echo.
echo Installing Python dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo [OK] Python dependencies installed

cd ..

echo.
echo ========================================
echo  Setting up Frontend
echo ========================================
echo.

cd frontend

echo Installing npm dependencies (this may take a few minutes)...
call npm install
echo [OK] npm dependencies installed

cd ..

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Start the backend (in a new terminal):
echo    cd backend
echo    venv\Scripts\activate.bat
echo    uvicorn main:app --reload
echo.
echo 2. Start the frontend (in another new terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 3. Access your applications:
echo    Frontend:    http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Docs:    http://localhost:8000/api/docs
echo    MinIO:       http://localhost:9001
echo    Mailhog:     http://localhost:8025
echo.
echo ========================================
echo.
pause
