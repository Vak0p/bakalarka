@echo off
cd /d "%~dp0"
set "PYTHON=%~dp0venv\Scripts\python.exe"
set "UIC=%~dp0venv\Lib\site-packages\PySide6\uic.exe"

if not exist "%PYTHON%" (
    echo Virtual environment not found. Create it and install requirements first.
    exit /b 1
)

if not exist "%UIC%" (
    echo PySide6 UI compiler not found. Install dependencies from requirements.txt.
    exit /b 1
)

"%UIC%" -g python ui/main_window.ui -o ui/main_window_ui.py
if errorlevel 1 exit /b %errorlevel%

"%PYTHON%" app.py