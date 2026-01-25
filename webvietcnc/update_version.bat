@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================================
echo CẬP NHẬT VERSION - VIETCNC
echo ============================================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python chưa được cài đặt!
    echo.
    echo Bạn có thể:
    echo 1. Cài Python từ: https://www.python.org/downloads/
    echo 2. Hoặc cập nhật thủ công file update.json
    echo.
    pause
    exit /b 1
)

REM Chạy script
python update_version.py

echo.
echo ============================================================
echo BẤM PHÍM BẤT KỲ ĐỂ MỞ GITHUB UPLOAD PAGE
echo ============================================================
pause >nul

REM Mở browser đến trang upload
start https://github.com/hotboy17894/VIETCNC/upload/main

echo.
echo ✓ Đã mở trình duyệt!
echo.
pause
