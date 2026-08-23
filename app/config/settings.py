"""Application configuration: data directory, persisted settings, first-run state."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from app.config.platform_paths import resolve_platform_data_dir

SETTINGS_FILENAME = "settings.json"
DB_FILENAME = "progress.sqlite3"


def get_data_dir() -> Path:
    return resolve_platform_data_dir()


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
