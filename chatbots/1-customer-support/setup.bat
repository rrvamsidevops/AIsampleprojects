@echo off
REM Setup script for Windows
REM Creates virtual environment and installs dependencies

setlocal enabledelayedexpansion

echo 🚀 Setting up Customer Support Chatbot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9 or later.
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ %PYTHON_VERSION% found
echo.

REM Create virtual environment
if exist venv (
    echo ⚠️  Virtual environment already exists. Skipping creation.
) else (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📥 Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt --quiet

echo.
echo ✅ Setup complete!
echo.
echo 📋 Next steps:
echo    1. Activate the environment: venv\Scripts\activate.bat
echo    2. Configure AWS credentials: aws configure
echo    3. Run the chatbot: python app.py
echo.

pause
