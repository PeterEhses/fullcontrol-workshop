@echo off
SETLOCAL EnableDelayedExpansion

SET "SCRIPT_DIR=%~dp0"
SET "MINICONDA_DIR=%SCRIPT_DIR%Miniconda3"

REM Check if setup has been run
IF NOT EXIST "%MINICONDA_DIR%\Scripts\conda.exe" (
    echo ========================================
    echo First Time Setup Required
    echo ========================================
    echo.
    echo Please run setup_windows.bat first to install Miniconda
    echo and create the workshop environment.
    echo.
    pause
    exit /b 1
)

REM Check if environment exists
CALL "%MINICONDA_DIR%\Scripts\activate.bat" fullcontrol_env 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo ========================================
    echo Environment Not Found
    echo ========================================
    echo.
    echo Please run setup_windows.bat to create the fullcontrol_env environment.
    echo.
    pause
    exit /b 1
)

echo Starting FullControl Workshop...
echo.

REM Check if a lesson argument was provided, otherwise use lesson-01
SET "LESSON=%~1"
IF "%LESSON%"=="" SET "LESSON=lesson-01-spiral-explorations"

SET "LESSON_PATH=%SCRIPT_DIR%lessons\%LESSON%\notebook.py"

REM Check if lesson exists
IF NOT EXIST "%LESSON_PATH%" (
    echo Lesson not found: %LESSON%
    echo Using default lesson-01...
    SET "LESSON_PATH=%SCRIPT_DIR%lessons\lesson-01-spiral-explorations\notebook.py"
)

REM Launch Marimo with the lesson notebook
marimo edit "%LESSON_PATH%"