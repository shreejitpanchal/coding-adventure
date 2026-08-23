"""Resolves the writable directory this app's data lives in -- a `data/`
folder inside the project itself, not an OS-appropriate per-user
directory. This app is run from a git checkout rather than installed as
a packaged product, so keeping progress alongside the code (easy to
find, easy to back up, no platform-specific path to look up) is more
useful here than the usual per-user-profile convention."""
from __future__ import annotations

from pathlib import Path

DATA_DIRNAME = "data"


def resolve_platform_data_dir() -> Path:
    """Returns <repo_root>/data, creating it if it doesn't exist yet."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    data_dir = repo_root / DATA_DIRNAME
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
