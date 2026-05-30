@echo off
chcp 65001 >nul
title OBS Server - Hieu Bui BDS
color 0A
cls

echo.
echo ============================================
echo   OBS SERVER - HIEU BUI BDS 24H
echo ============================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Install Python: https://www.python.org/downloads/
    echo Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo [OK] %PYTHON_VER%
echo.

cd /d "%~dp0"

if not exist "server.py" (
    echo [ERROR] server.py not found!
    pause
    exit /b 1
)

echo [OK] server.py found
echo.
echo ============================================
echo SERVER RUNNING AT:
echo ============================================
echo.
echo Chrome (Control):
echo   http://localhost:8765/ok_khung_live_v2.html
echo.
echo OBS Browser Source:
echo   http://localhost:8765/ok_khung_live_v2.html?obs=1
echo.
echo Server API:
echo   GET  http://localhost:8765/api/config
echo   POST http://localhost:8765/api/config
echo.
echo Config File: config.json
echo.
echo ============================================
echo.
echo Press Ctrl+C to stop server
echo.
echo ============================================
echo.

python server.py

pause
