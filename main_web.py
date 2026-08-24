"""Web entry point for Coding Adventure -- a one-off browser preview of the
UI, not a supported way to actually run exercises (see CLAUDE.md: this app
is desktop-only by design, since exercises need real local compiler/
interpreter subprocesses a browser sandbox can't provide). Useful for
reviewing screens in Chrome/etc. without a native window.

Port is configurable via the CODING_ADVENTURE_WEB_PORT environment
variable (default 8550) -- see run_app_web_ui.bat/.sh, or set it yourself
before running this directly."""
from __future__ import annotations

import os

import flet as ft

from app.ui.app_window import main

PORT = int(os.environ.get("CODING_ADVENTURE_WEB_PORT", "8550"))

ft.run(main, view=ft.AppView.WEB_BROWSER, host="localhost", port=PORT)
