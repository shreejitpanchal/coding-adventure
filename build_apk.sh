#!/usr/bin/env bash
# Builds an Android APK from main.py -- `flet build` drives a real Flutter
# SDK + Android SDK/NDK under the hood; see
# https://flet.dev/docs/publish/android for first-time toolchain setup.
# This script assumes that's already installed and just runs the build.
#
# Android support is Python-only: PythonInProcessEngine
# (app/execution/python_inprocess_engine.py) runs submitted code in-process
# instead of PythonEngine's usual `python -I` subprocess, since a
# non-rooted Android app can't spawn a sibling OS process at all -- see
# app/execution/registry.py, which swaps to it automatically whenever
# app/execution/android_platform.is_android() is true. Java, C++, and
# Spring need a real javac/g++/mvn toolchain that can't exist on Android
# and can't be bundled into an app sandbox -- they simply won't find their
# toolchain there, and the language picker shows them as "Desktop only"
# rather than the desktop install-guide dialog (see language_select.py).
# --module-name is NOT needed here (unlike python-adventure-kids' own
# build_apk.sh): `flet build` already defaults to looking for main.py,
# and that's genuinely this app's real Flet entry point, with no naming
# conflict to work around.
set -e

cd "$(dirname "${BASH_SOURCE[0]}")"

venv_bin() {
    # $1: posix-style script name without extension, e.g. "python" or "flet"
    if [ -f ".venv/Scripts/$1.exe" ]; then
        echo ".venv/Scripts/$1.exe"
    elif [ -f ".venv/bin/$1" ]; then
        echo ".venv/bin/$1"
    else
        echo ""
    fi
}

PYEXE="$(venv_bin python)"
FLETEXE="$(venv_bin flet)"

if [ -z "$PYEXE" ]; then
    echo "No .venv found -- run run_app_window_mode.bat/.sh once first to set it up."
    exit 1
fi

if [ -z "$FLETEXE" ]; then
    echo "flet isn't available in .venv -- run run_app_window_mode.bat/.sh once"
    echo "first (or pip install -r requirements.txt) to set it up."
    exit 1
fi

# `flutter` isn't a pip dependency -- flet build shells out to a real
# Flutter SDK install, which isn't guaranteed to be on PATH. Look there
# first, then fall back to $FLUTTER_HOME, then this machine's known
# install location as a last resort.
if ! command -v flutter >/dev/null 2>&1; then
    if [ -n "$FLUTTER_HOME" ] && [ -x "$FLUTTER_HOME/bin/flutter" ]; then
        export PATH="$FLUTTER_HOME/bin:$PATH"
    elif [ -x "$HOME/flutter/3.44.8/bin/flutter" ]; then
        export PATH="$HOME/flutter/3.44.8/bin:$PATH"
    else
        echo "Flutter SDK not found on PATH."
        echo "Install it (https://docs.flutter.dev/get-started/install), then either"
        echo "put its bin/ on PATH or set FLUTTER_HOME to the SDK root and re-run."
        exit 1
    fi
fi

# BUILD_NUMBER is a plain repo-root file holding a single integer, bumped
# on every build -- Android requires a build's versionCode to strictly
# increase between installs of the same package, so this file is what
# guarantees that across repeated builds even though this app has no
# in-app version display (unlike python-adventure-kids, which reads this
# same convention back out in Settings).
BUILD_NUMBER_FILE="BUILD_NUMBER"
if [ -f "$BUILD_NUMBER_FILE" ]; then
    PREV_BUILD="$(cat "$BUILD_NUMBER_FILE")"
else
    PREV_BUILD=0
fi
NEW_BUILD=$((PREV_BUILD + 1))
echo "$NEW_BUILD" > "$BUILD_NUMBER_FILE"

# Read [project].version out of pyproject.toml (stdlib tomllib) so the
# APK filename and the --build-version passed to Flutter can never drift
# from what's declared there.
APP_VERSION="$("$PYEXE" -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")"

echo "Building Android APK from main.py (v$APP_VERSION build $NEW_BUILD)..."
echo "Python track only -- Java/C++/Spring need a desktop toolchain and"
echo "aren't available in this build (see language_select.py)."
echo

# flet build's own CLI output (via `rich`) includes emoji (checkmarks
# etc.); on Windows, a subprocess's stdout can default to the legacy
# cp1252 console codepage instead of UTF-8, which crashes on those
# characters before the build even starts. Force UTF-8 regardless of the
# console's codepage.
export PYTHONUTF8=1

"$FLETEXE" build apk --yes \
    --build-number "$NEW_BUILD" --build-version "$APP_VERSION" "$@"

TAGGED_APK="build/apk/coding-adventure-v${APP_VERSION}-build${NEW_BUILD}.apk"
mv "build/apk/coding-adventure.apk" "$TAGGED_APK"

echo
echo "Done -- APK at $TAGGED_APK"
