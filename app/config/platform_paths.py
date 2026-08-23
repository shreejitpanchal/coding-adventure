"""Resolves the real, writable directory this app's data lives in."""
from __future__ import annotations

import os
import sys
from pathlib import Path

APP_FOLDER_NAME = "CodingAdventure"


def resolve_platform_data_dir() -> Path:
    """Returns the OS-appropriate writable data directory, creating it if
    it doesn't exist yet."""
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        data_dir = (Path(appdata) if appdata else Path.home()) / APP_FOLDER_NAME
    else:
        data_dir = Path.home() / f".{APP_FOLDER_NAME.lower()}"

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
