@echo off
call .venv\Scripts\activate.bat
if "%1"=="web" (
    python run_web.py
) else (
    paperscraper %*
) 