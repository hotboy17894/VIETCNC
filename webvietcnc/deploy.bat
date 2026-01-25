@echo off
chcp 65001 >nul
echo ============================================================
echo VIETCNC AUTO DEPLOY TOOL
echo ============================================================
echo.

REM Kiểm tra Python đã cài chưa
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python chưa được cài đặt!
    echo Vui lòng cài Python từ: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Chạy script Python
python deploy.py

echo.
pause
