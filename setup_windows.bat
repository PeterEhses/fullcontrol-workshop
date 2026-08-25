@echo off
REM One-time setup. Installs uv if you don't have it, then the workshop dependencies.
cd /d "%~dp0"

where uv >nul 2>nul
if errorlevel 1 (
    echo Installing uv...
    powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;%PATH%"
)

echo Installing dependencies ^(this downloads Python too, if needed^)...
uv sync
if errorlevel 1 (
    echo.
    echo Setup failed. Check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Done. Now double-click run_windows.bat
pause
