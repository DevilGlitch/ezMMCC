@echo off
setlocal

rem Check if ezMMCC.py exists
if not exist "ezMMCC.py" (
    echo ezMMCC.py does not exist. Downloading from GitHub...
    curl -o "ezMMCC.py" "https://raw.githubusercontent.com/DevilGlitch/ezMMCC/main/ezMMCC.py"
)

rem Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip is not installed. Please install Python with Pip.
    exit /b 1
)

rem Install required Python packages
echo Installing required Python packages...
pip install psutil tkinter

echo Installation complete.

rem Run ezMMCC.py
python ezMMCC.py

endlocal
