@echo off
REM Navigate to the script directory (dynamic path)
cd /d "%~dp0"

REM Activate the virtual environment
call venv\Scripts\activate

REM Define a temporary Python script to read the JSON configuration
setlocal enabledelayedexpansion
echo import json > temp_config_reader.py
echo with open('config.json', 'r') as f: >> temp_config_reader.py
echo     config = json.load(f) >> temp_config_reader.py
echo model = config.get('model', 'default') >> temp_config_reader.py
echo if model == 'yolo': >> temp_config_reader.py
echo     print('yolo') >> temp_config_reader.py
echo elif model == 'default': >> temp_config_reader.py
echo     print('default') >> temp_config_reader.py

REM Run the temporary Python script to determine which script to run
for /f "tokens=*" %%i in ('python temp_config_reader.py') do set script_to_run=%%i

REM Run the appropriate Python script
if "%script_to_run%"=="yolo" (
    python yolo.py
) else (
    python music.py
)

REM Clean up temporary Python script
del temp_config_reader.py

REM Deactivate the virtual environment
deactivate
