@echo off
SETLOCAL EnableDelayedExpansion

echo ========================================
echo FullControl Workshop Setup - Windows
echo ========================================
echo.

REM Get the directory where this script is located
SET "SCRIPT_DIR=%~dp0"
SET "MINICONDA_DIR=%SCRIPT_DIR%Miniconda3"
SET "INSTALLER=%SCRIPT_DIR%miniconda_installer.exe"

REM Check if Miniconda is already installed in the workshop folder
IF EXIST "%MINICONDA_DIR%\Scripts\conda.exe" (
    echo [OK] Miniconda already installed locally
    goto CREATE_ENV
)

echo [1/3] Downloading Miniconda installer...
echo This may take a few minutes...
powershell -Command "& {Invoke-WebRequest -Uri 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe' -OutFile '%INSTALLER%'}"

IF NOT EXIST "%INSTALLER%" (
    echo [ERROR] Failed to download Miniconda installer
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo [OK] Download complete
echo.

echo [2/3] Installing Miniconda locally (this takes a few minutes)...
echo Installing to: %MINICONDA_DIR%
start /wait "" "%INSTALLER%" /InstallationType=JustMe /RegisterPython=0 /S /D=%MINICONDA_DIR%

IF NOT EXIST "%MINICONDA_DIR%\Scripts\conda.exe" (
    echo [ERROR] Miniconda installation failed
    pause
    exit /b 1
)

echo [OK] Miniconda installed
del "%INSTALLER%"
echo.

:CREATE_ENV
echo [3/3] Creating fullcontrol_env environment...

REM Check if environment already exists
CALL "%MINICONDA_DIR%\Scripts\activate.bat" fullcontrol_env 2>nul
IF %ERRORLEVEL% EQU 0 (
    echo [OK] Environment 'fullcontrol_env' already exists
    goto DONE
)

REM Create the environment
CALL "%MINICONDA_DIR%\Scripts\activate.bat"
CALL conda env create -f "%SCRIPT_DIR%environment.yml"

IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to create environment
    echo Please check environment.yml and try again
    pause
    exit /b 1
)

echo [OK] Environment created successfully
echo.

:DONE
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now run the workshop by double-clicking: run_windows.bat
echo.
pause
