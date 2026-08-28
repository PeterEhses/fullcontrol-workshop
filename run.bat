@echo off
REM Double-click       day 1, part A, as an app
REM run.bat 1 b        day 1, part b  (run.bat 1b works too)
REM run.bat 3 e1       day 3, the first exercise
REM run.bat browse     the marimo editor with the file sidebar
REM
REM Names are matched by prefix, so as long as it's unique, as little as you like.
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "APP_NOTEBOOK=lessons\1-tiles\a-points.py"

if "%~1"=="" (
    uv run marimo run "%APP_NOTEBOOK%"
    pause
    exit /b 0
)

if /i "%~1"=="browse" (
    uv run marimo edit .
    exit /b 0
)

set "DAY=%~1"
set "PART=%~2"

REM "1b" as one word, as long as it isn't a full folder name like "1-tiles"
if "%PART%"=="" (
    set "REST=%DAY:~1%"
    if not "!REST!"=="" if not "!REST:~0,1!"=="-" (
        set "PART=!REST!"
        set "DAY=%DAY:~0,1%"
    )
)

set "DIR="
set /a MATCHES=0
for /d %%D in ("lessons\%DAY%*") do (
    set /a MATCHES+=1
    set "DIR=%%D"
)

if !MATCHES!==0 (
    echo No day matching "%DAY%". Available:
    dir /b lessons
    pause
    exit /b 1
)
if !MATCHES! GTR 1 (
    echo "%DAY%" matches more than one day:
    for /d %%D in ("lessons\%DAY%*") do echo    %%~nxD
    pause
    exit /b 1
)

if "%PART%"=="" (
    echo Which notebook? In !DIR!:
    for %%F in ("!DIR!\*.py") do echo    %%~nF
    pause
    exit /b 1
)

set "NOTEBOOK="
set /a HITS=0
for %%F in ("!DIR!\%PART%*.py") do (
    set /a HITS+=1
    set "NOTEBOOK=%%F"
)

if !HITS!==0 (
    echo Nothing matching "%PART%" in !DIR!:
    for %%F in ("!DIR!\*.py") do echo    %%~nF
    pause
    exit /b 1
)
if !HITS! GTR 1 (
    echo "%PART%" matches more than one notebook:
    for %%F in ("!DIR!\%PART%*.py") do echo    %%~nF
    pause
    exit /b 1
)

REM a-points is the one notebook meant to be driven rather than read
if /i "!NOTEBOOK!"=="%APP_NOTEBOOK%" if not "%~3"=="edit" (
    uv run marimo run "!NOTEBOOK!"
    pause
    exit /b 0
)

uv run marimo edit "!NOTEBOOK!"
pause
