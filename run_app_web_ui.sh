#!/usr/bin/env bash
# Launches Coding Adventure as a one-off browser preview (not the primary
# way to use the app -- see main_web.py's docstring). Sets up the virtual
# environment on first run, same as run_app_window_mode.sh.
#
# Port is configurable via CODING_ADVENTURE_WEB_PORT (default 8550):
#   CODING_ADVENTURE_WEB_PORT=9000 ./run_app_web_ui.sh
set -e

cd "$(dirname "${BASH_SOURCE[0]}")"

venv_python() {
    if [ -f ".venv/Scripts/python.exe" ]; then
        echo ".venv/Scripts/python.exe"
    elif [ -f ".venv/bin/python" ]; then
        echo ".venv/bin/python"
    else
        echo ""
    fi
}

PYEXE="$(venv_python)"

if [ -z "$PYEXE" ]; then
    echo "============================================"
    echo "  Setting up Coding Adventure for the"
    echo "  first time. This only happens once and"
    echo "  may take a minute..."
    echo "============================================"
    echo

    if command -v python >/dev/null 2>&1; then
        PY=python
    elif command -v python3 >/dev/null 2>&1; then
        PY=python3
    else
        echo "Python was not found on this computer."
        echo "Please install Python from https://python.org then run this again."
        read -p "Press Enter to close..."
        exit 1
    fi

    "$PY" -m venv .venv
    PYEXE="$(venv_python)"

    "$PYEXE" -m pip install --upgrade pip
    "$PYEXE" -m pip install -r requirements.txt

    echo
    echo "Setup complete!"
    echo
fi

: "${CODING_ADVENTURE_WEB_PORT:=8550}"
export CODING_ADVENTURE_WEB_PORT

# Ctrl+C on a previous run doesn't always kill the underlying Python
# process cleanly -- it can be left listening on the port, which then
# makes the next launch fail with a confusing asyncio traceback instead
# of a clear "port in use" message. Self-heal: if a leftover Python
# process still owns the port, stop it before we start.
port_owner_pid() {
    if command -v lsof >/dev/null 2>&1; then
        lsof -ti tcp:"$1" -sTCP:LISTEN 2>/dev/null | head -n1
    elif command -v netstat >/dev/null 2>&1; then
        netstat -ano 2>/dev/null | awk -v p=":$1" '$0 ~ p && $0 ~ /LISTENING/ {print $NF; exit}'
    fi
}

is_python_process() {
    if command -v ps >/dev/null 2>&1 && ps -p "$1" -o comm= >/dev/null 2>&1; then
        ps -p "$1" -o comm= | grep -qi python
    elif command -v powershell.exe >/dev/null 2>&1; then
        powershell.exe -NoProfile -Command "(Get-Process -Id $1 -ErrorAction SilentlyContinue).ProcessName" 2>/dev/null | grep -qi python
    else
        return 1
    fi
}

EXISTING_PID="$(port_owner_pid "$CODING_ADVENTURE_WEB_PORT")"
if [ -n "$EXISTING_PID" ]; then
    if is_python_process "$EXISTING_PID"; then
        echo "Stopping a leftover Coding Adventure instance on port $CODING_ADVENTURE_WEB_PORT (PID $EXISTING_PID)..."
        kill -9 "$EXISTING_PID" 2>/dev/null \
            || (command -v powershell.exe >/dev/null 2>&1 && powershell.exe -NoProfile -Command "Stop-Process -Id $EXISTING_PID -Force" 2>/dev/null) \
            || true
        sleep 1
    else
        echo "Warning: port $CODING_ADVENTURE_WEB_PORT is already in use by PID $EXISTING_PID, which is not a Python process -- leaving it alone."
        echo "Set CODING_ADVENTURE_WEB_PORT to a free port instead."
    fi
fi

echo "============================================"
echo "  Coding Adventure web UI starting on port $CODING_ADVENTURE_WEB_PORT"
echo "  Open http://localhost:$CODING_ADVENTURE_WEB_PORT in your browser."
echo "  (Set CODING_ADVENTURE_WEB_PORT before running this to use a"
echo "  different port.)"
echo "  Press Ctrl+C to stop."
echo "============================================"
echo

"$PYEXE" main_web.py
