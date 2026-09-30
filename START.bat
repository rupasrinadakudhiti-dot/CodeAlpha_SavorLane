@echo off
setlocal
cd /d "%~dp0"
title SavorLane - Local Server

echo ========================================
echo   SavorLane - Food Store Demo
echo ========================================

if not exist ".venv\Scripts\python.exe" (
    echo Creating Python environment...
    where py >nul 2>&1
    if not errorlevel 1 (
        py -3 -m venv .venv
    ) else (
        python -m venv .venv
    )
    if errorlevel 1 goto :fail
)

set "PROJECT_PYTHON=%CD%\.venv\Scripts\python.exe"
if not exist "%PROJECT_PYTHON%" goto :fail

echo Installing Python packages...
"%PROJECT_PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 goto :fail

echo Preparing the database...
"%PROJECT_PYTHON%" manage.py migrate --noinput
if errorlevel 1 goto :fail

echo Loading sample food menu...
"%PROJECT_PYTHON%" manage.py seed_data
if errorlevel 1 goto :fail

echo.
echo Open http://127.0.0.1:8000/ in your browser.
echo Register a new account to place a demo order.
echo Press Ctrl+C to stop the server.
echo.
"%PROJECT_PYTHON%" manage.py runserver 127.0.0.1:8000
pause
exit /b 0

:fail
echo.
echo Setup failed. Read the error above, then run START.bat again.
pause
exit /b 1
