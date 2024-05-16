@echo off
REM Batch script to install dependencies and run ezMMCC.py

REM Set the URL to download ezMMCC.py if not found
set "URL=https://raw.githubusercontent.com/DevilGlitch/ezMMCC/main/ezMMCC.py"

REM Check for Python installation
echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python before running this script.
    pause
    exit /b
)

REM Install required Python packages
echo Installing required Python packages...
pip install psutil tkinter >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to install required packages. Please check your Python and pip installation.
    pause
    exit /b
)

REM Check if ezMMCC.py exists
if not exist "ezMMCC.py" (
    echo ezMMCC.py not found. Downloading...
    powershell -Command "Invoke-WebRequest -Uri %URL% -OutFile ezMMCC.py"
    if %errorlevel% neq 0 (
        echo Failed to download ezMMCC.py. Please check your internet connection and URL.
        pause
        exit /b
    )
)

REM Run ezMMCC.py
echo Running ezMMCC.py...
python ezMMCC.py
if %errorlevel% neq 0 (
    echo Failed to run ezMMCC.py. Please check the script for errors.
    pause
    exit /b
)

echo Script completed successfully.
pause
