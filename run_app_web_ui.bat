@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ============================================
    echo   Setting up Coding Adventure for the
    echo   first time. This only happens once and
    echo   may take a minute...
    echo ============================================
    echo.

    where python >nul 2>nul
    if errorlevel 1 (
        echo Python was not found on this computer.
        echo Please install Python from https://python.org
        echo then run this file again.
        echo.
        pause
        exit /b 1
    )

    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo Something went wrong creating the Python environment.
        echo.
        pause
        exit /b 1
    )

    ".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Something went wrong installing the required packages.
        echo.
        pause
        exit /b 1
    )

    echo.
    echo Setup complete!
    echo.
)

if "%CODING_ADVENTURE_WEB_PORT%"=="" set CODING_ADVENTURE_WEB_PORT=8550

echo ============================================
echo   Coding Adventure web UI starting on port %CODING_ADVENTURE_WEB_PORT%
echo   Open http://localhost:%CODING_ADVENTURE_WEB_PORT% in your browser.
echo   (Set CODING_ADVENTURE_WEB_PORT before running this to use a
echo   different port.)
echo   Press Ctrl+C to stop.
echo ============================================
echo.

".venv\Scripts\python.exe" "main_web.py"
