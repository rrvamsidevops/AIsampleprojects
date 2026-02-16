@echo off
REM Setup script for Multi-Intent Chatbot (Windows)

echo Setting up Multi-Intent Chatbot...

REM Create virtual environment
python -m venv venv
echo [OK] Virtual environment created

REM Activate virtual environment
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated

REM Upgrade pip
python -m pip install --upgrade pip > nul 2>&1
echo [OK] pip upgraded

REM Install dependencies
pip install -r requirements.txt > nul 2>&1
echo [OK] Dependencies installed

REM Create .env file if it doesn't exist
if not exist .env (
    (
        echo AWS_REGION=us-east-1
        echo AWS_ACCESS_KEY_ID=your_access_key_here
        echo AWS_SECRET_ACCESS_KEY=your_secret_key_here
        echo LOG_LEVEL=INFO
    ) > .env
    echo [OK] .env file created (update with your AWS credentials)
) else (
    echo [OK] .env file already exists
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Update .env with your AWS credentials
echo 2. Activate venv: venv\Scripts\activate
echo 3. Run tests: python -m pytest test_chatbot.py -v
echo 4. Run app: python app.py
