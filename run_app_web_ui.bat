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

if "%CODING_ADVENTURE_WEB_PORT%"=="" set CODING_ADVENTURE_WEB_PORT=8550

REM Ctrl+C on a previous run doesn't always kill the underlying Python
REM process cleanly on Windows -- it can be left listening on the port,
REM which then makes the next launch fail with a confusing asyncio
REM traceback instead of a clear "port in use" message. Self-heal: if a
REM leftover Python process still owns the port, stop it before we start.
powershell -NoProfile -Command "$conns = Get-NetTCPConnection -LocalPort %CODING_ADVENTURE_WEB_PORT% -State Listen -ErrorAction SilentlyContinue; foreach ($procId in ($conns.OwningProcess | Sort-Object -Unique)) { $p = Get-Process -Id $procId -ErrorAction SilentlyContinue; if ($p -and $p.ProcessName -match '^python') { Write-Host ('Stopping a leftover Coding Adventure instance on port %CODING_ADVENTURE_WEB_PORT% (PID ' + $procId + ')...'); Stop-Process -Id $procId -Force } elseif ($p) { Write-Host ('Warning: port %CODING_ADVENTURE_WEB_PORT% is already in use by PID ' + $procId + ' (' + $p.ProcessName + '), which is not a Python process -- leaving it alone. Set CODING_ADVENTURE_WEB_PORT to a free port instead.') } }"

echo ============================================
echo   Coding Adventure web UI starting on port %CODING_ADVENTURE_WEB_PORT%
echo   Open https://localhost:%CODING_ADVENTURE_WEB_PORT% in your browser
echo   (opens automatically). It's a self-signed certificate, so your
echo   browser will show a one-time warning -- click "Advanced" then
echo   "Proceed to localhost" to continue.
echo   (Set CODING_ADVENTURE_WEB_PORT before running this to use a
echo   different port.)
echo   Press Ctrl+C to stop.
echo ============================================
echo.

".venv\Scripts\python.exe" "main_web.py"
