@echo off
setlocal enabledelayedexpansion

echo Checking Python installation...
if not exist "C:\Program Files\Python313\python.exe" (
    echo Python not found at C:\Program Files\Python313\python.exe
    echo Please make sure Python is installed correctly
    pause
    exit /b 1
)

echo Creating virtual environment...
"C:\Program Files\Python313\python.exe" -m venv .venv
if errorlevel 1 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip
    pause
    exit /b 1
)

echo Installing package...
pip install -e ".[dev]"
if errorlevel 1 (
    echo Failed to install package
    pause
    exit /b 1
)

echo Setup completed successfully!
echo.
echo To run the script, use:
echo paperscraper "your search term"
echo.
pause 