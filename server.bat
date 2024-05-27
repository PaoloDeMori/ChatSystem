@echo off

python3 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    python3 server.py
) else (
    echo Python3 non è installato
)
