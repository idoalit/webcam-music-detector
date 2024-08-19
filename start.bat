@echo off
REM Navigate to the script directory (dynamic path)
cd /d "%~dp0"

REM Activate the virtual environment
call venv\Scripts\activate

REM Run the Python script
python music.py

REM Deactivate the virtual environment
deactivate
