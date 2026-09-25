"""Application logging: a rotating plain-text log under the data directory.

Flet swallows exceptions raised inside event handlers -- without a log
file there is nothing to look at when a screen misbehaves. Both entry
points (main.py, main_web.py) call configure_logging() once at startup;
modules then use the stdlib pattern `logger = logging.getLogger(__name__)`.

Kept deliberately small: no third-party logging library, no JSON, no
telemetry. The log holds file paths and exercise ids, never the user's
submitted code in full (engines log only outcome flags), and never
anything from settings.json beyond the theme/font keys."""
from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path

LOG_DIRNAME = "logs"
LOG_FILENAME = "app.log"
_MAX_BYTES = 1_000_000
_BACKUP_COUNT = 3
_FORMAT = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"


def configure_logging(data_dir: Path, level: int = logging.INFO) -> Path:
    """Attach a rotating file handler to the root logger (idempotent --
    a second call with the same directory adds nothing). Returns the log
    file path so a caller can print it."""
    log_dir = data_dir / LOG_DIRNAME
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / LOG_FILENAME

    root = logging.getLogger()
    root.setLevel(level)
    already = any(
        isinstance(h, logging.handlers.RotatingFileHandler)
        and Path(getattr(h, "baseFilename", "")) == log_path
        for h in root.handlers
    )
    if not already:
        handler = logging.handlers.RotatingFileHandler(
            log_path, maxBytes=_MAX_BYTES, backupCount=_BACKUP_COUNT, encoding="utf-8",
        )
        handler.setFormatter(logging.Formatter(_FORMAT))
        root.addHandler(handler)
    return log_path
