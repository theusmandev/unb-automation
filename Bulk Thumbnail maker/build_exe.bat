@echo off
echo ========================================
echo  Bulk Thumbnail Maker - EXE Builder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Installing required dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Building executable with PyInstaller...
pyinstaller --clean build_exe.spec

echo.
echo [3/3] Build complete!
echo.
echo ========================================
echo  Your executable is ready!
echo ========================================
echo Location: dist\BulkThumbnailMaker.exe
echo.
echo You can now run the .exe file directly without Python installed!
echo.
pause
