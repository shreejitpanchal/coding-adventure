"""Application configuration: data directory, persisted settings, first-run state."""
from __future__ import annotations

import json
import os
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from app.config.platform_paths import resolve_platform_data_dir

SETTINGS_FILENAME = "settings.json"
DB_FILENAME = "progress.sqlite3"

# Storage lived in an OS-appropriate per-user directory (%APPDATA%\CodingAdventure
# on Windows) before moving to a project-local data/ folder. _migrate_from_legacy_dir()
# copies anything found there forward, once, so switching storage location never
# resets a user's progress -- see resolve_platform_data_dir()'s docstring for why
# project-local is now preferred.
_LEGACY_APP_FOLDER_NAME = "CodingAdventure"


def _legacy_platform_data_dir() -> Path:
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        return (Path(appdata) if appdata else Path.home()) / _LEGACY_APP_FOLDER_NAME
    return Path.home() / f".{_LEGACY_APP_FOLDER_NAME.lower()}"


def _migrate_from_legacy_dir(data_dir: Path) -> None:
    """One-time copy from the old per-user platform directory. Never
    overwrites a file that already exists at the destination."""
    old_dir = _legacy_platform_data_dir()
    if old_dir == data_dir or not old_dir.is_dir():
        return
    for filename in (SETTINGS_FILENAME, DB_FILENAME):
        old_file = old_dir / filename
        new_file = data_dir / filename
        if old_file.is_file() and not new_file.exists():
            shutil.copy2(old_file, new_file)


def get_data_dir() -> Path:
    data_dir = resolve_platform_data_dir()
    _migrate_from_legacy_dir(data_dir)
    return data_dir


def get_db_path() -> Path:
    return get_data_dir() / DB_FILENAME


def get_settings_path() -> Path:
    return get_data_dir() / SETTINGS_FILENAME


@dataclass
class Settings:
    handle: str = ""
    """The user's display name -- not gated behind an account, purely local."""
    theme: str = "one_dark"
    code_font_size: str = "medium"
    """One of small/medium/large -- see app/ui/theme.py's FONT_SIZE_SCALES."""
    setup_complete: bool = False
    last_selected_language: str = ""
    """Pre-highlights a card on the language picker -- never used to
    auto-route past it; the picker is shown on every launch by design."""

    def has_handle(self) -> bool:
        return bool(self.handle)


def load_settings() -> Settings:
    path = get_settings_path()
    if not path.exists():
        return Settings()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return Settings()
    known_fields = {f for f in Settings.__dataclass_fields__}
    filtered = {k: v for k, v in data.items() if k in known_fields}
    return Settings(**filtered)


def save_settings(settings: Settings) -> None:
    path = get_settings_path()
    path.write_text(json.dumps(asdict(settings), indent=2), encoding="utf-8")


def is_first_run() -> bool:
    return not load_settings().setup_complete
