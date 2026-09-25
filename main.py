"""Entry point for Coding Adventure. Run with `python main.py`."""
from __future__ import annotations

import flet as ft

from app.config.logging_setup import configure_logging
from app.config.settings import get_data_dir
from app.ui.app_window import main

configure_logging(get_data_dir())
ft.run(main)
