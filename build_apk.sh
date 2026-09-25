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
# toolchain there, and the language picker still shows them as "Available"
# (subtitle explains Run needs a desktop computer) rather than the desktop
# install-guide dialog (see language_select.py); every category/level in
# those three tracks is also unlocked on Android since completion is never
# reachable there (see ExerciseEngine.is_unlocked in lesson_engine.py).
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

# `flutter` isn't a pip dependency. Prefer an SDK already on PATH, then
# $FLUTTER_HOME, then the copy flet itself manages. If none exists, do NOT
# stop: `flet build` downloads the Flutter SDK it needs (the version
# pinned by the installed flet, into ~/flutter/<version>) and a JDK (into
# ~/java) on first use. That first run needs network access and several
# minutes; every later build reuses the same install.
FLET_FLUTTER_VERSION="$("$PYEXE" -c "import flet.version as v; print(v.flutter_version)" 2>/dev/null || true)"
if ! command -v flutter >/dev/null 2>&1; then
    if [ -n "$FLUTTER_HOME" ] && [ -x "$FLUTTER_HOME/bin/flutter" ]; then
        export PATH="$FLUTTER_HOME/bin:$PATH"
    elif [ -n "$FLET_FLUTTER_VERSION" ] && [ -x "$HOME/flutter/$FLET_FLUTTER_VERSION/bin/flutter" ]; then
        export PATH="$HOME/flutter/$FLET_FLUTTER_VERSION/bin:$PATH"
    else
        echo "No Flutter SDK on PATH or in FLUTTER_HOME -- flet build will download"
        echo "Flutter ${FLET_FLUTTER_VERSION:-(pinned version)} into $HOME/flutter and a JDK into $HOME/java."
        echo "First run: several minutes and ~1 GB of downloads. Later builds reuse them."
        echo
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
