"""Resolves the writable directory this app's data lives in.

On desktop/web this is a `data/` folder inside the project itself, not
an OS-appropriate per-user directory -- this app is run from a git
checkout rather than installed as a packaged product, so keeping
progress alongside the code (easy to find, easy to back up, no
platform-specific path to look up) is more useful here than the usual
per-user-profile convention.

That reasoning doesn't hold on Android at all: there is no "repo
checkout" a packaged APK is run from, and `<bundle>/data` may not even
be a reliably writable location (or a stable one across app updates).
Flet's own runtime sets `FLET_APP_STORAGE_DATA` on every packaged
target (Android included) to a real, writable, per-app directory
specifically for this purpose -- checked first here, same convention
the sibling kids' app already uses for its own Android build."""
from __future__ import annotations

import os
from pathlib import Path

DATA_DIRNAME = "data"


def resolve_platform_data_dir() -> Path:
    """Returns FLET_APP_STORAGE_DATA when set (packaged builds, e.g.
    Android), otherwise <repo_root>/data (desktop/web dev runs) --
    creating it if it doesn't exist yet either way."""
    android_dir = os.environ.get("FLET_APP_STORAGE_DATA")
    if android_dir:
        data_dir = Path(android_dir)
    else:
        repo_root = Path(__file__).resolve().parent.parent.parent
        data_dir = repo_root / DATA_DIRNAME

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
