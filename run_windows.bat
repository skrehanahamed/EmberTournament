@echo off
REM EMBER TOURNAMENT - double-click to play (Windows). Needs Python 3.10+ from python.org ("Add python.exe to PATH" ticked).
cd /d "%~dp0"
if not exist .venv (
    echo First start: installing the game's requirements, this takes a minute...
    python -m venv .venv || (echo Python was not found. Install it from https://www.python.org/downloads/ & pause & exit /b 1)
    .venv\Scripts\python -m pip install -q -r requirements.txt || (echo Install failed & pause & exit /b 1)
)
.venv\Scripts\python main.py %*
if errorlevel 1 pause
