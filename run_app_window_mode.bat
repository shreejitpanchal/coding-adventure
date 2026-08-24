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
) else (
    REM The venv already exists, but requirements.txt may have grown new
    REM dependencies since it was created (e.g. an update pulled from git)
    REM -- pip install is a fast no-op when everything's already satisfied,
    REM so it's cheap to just re-sync on every launch rather than silently
    REM running with a stale, incomplete venv.
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo.
        echo Warning: could not verify required packages are up to date
        echo ^(check your internet connection^). Continuing anyway --
        echo the app may fail to start if a new dependency is missing.
        echo.
    )
)

call "scripts\ensure_toolchains.bat"

if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" "main.py"
) else (
    start "" ".venv\Scripts\python.exe" "main.py"
)
