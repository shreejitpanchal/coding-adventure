#!/usr/bin/env bash
# Launches Coding Adventure as a native desktop window -- sets up the
# virtual environment on first run. For a one-off browser preview instead,
# see run_app_web_ui.sh.
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
else
    # The venv already exists, but requirements.txt may have grown new
    # dependencies since it was created (e.g. an update pulled from git) --
    # pip install is a fast no-op when everything's already satisfied, so
    # it's cheap to just re-sync on every launch rather than silently
    # running with a stale, incomplete venv.
    "$PYEXE" -m pip install -r requirements.txt --quiet || \
        echo "Warning: could not verify required packages are up to date (check your internet connection). Continuing anyway."
fi

bash "scripts/ensure_toolchains.sh" || true

"$PYEXE" main.py
