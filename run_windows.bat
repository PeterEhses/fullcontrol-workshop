@echo off
REM Double-click to open lesson 01 as an app.
REM From a terminal:  run_windows.bat 05-the-noodle
REM                   run_windows.bat 05-the-noodle edit
cd /d "%~dp0"

set "LESSON=%~1"
if "%LESSON%"=="" set "LESSON=01-the-path"

set "DIR=lessons\%LESSON%"
if not exist "%DIR%" set "DIR=%LESSON%"
if not exist "%DIR%" (
    echo No lesson called "%LESSON%". Available:
    dir /b lessons
    pause
    exit /b 1
)

set "NOTEBOOK="
for %%F in ("%DIR%\*.py") do if not defined NOTEBOOK set "NOTEBOOK=%%F"
if not defined NOTEBOOK (
    echo No notebook in %DIR%
    pause
    exit /b 1
)

if /i "%~2"=="edit" (
    uv run marimo edit "%NOTEBOOK%"
) else (
    uv run marimo run "%NOTEBOOK%"
)
pause
