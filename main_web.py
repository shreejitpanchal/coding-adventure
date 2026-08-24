"""Web entry point for Coding Adventure -- a one-off browser preview of the
UI, not a supported way to actually run exercises (see CLAUDE.md: this app
is desktop-only by design, since exercises need real local compiler/
interpreter subprocesses a browser sandbox can't provide). Useful for
reviewing screens in Chrome/etc. without a native window.

Served over HTTPS with a locally-generated, self-signed certificate
(CN=coding-adventure -- see app/config/ssl_cert.py) rather than plain
HTTP, so the connection itself is encrypted. Because the certificate isn't
issued by a trusted CA, the browser will still show a one-time
interstitial warning ("Your connection isn't private" / "This site can't
provide a secure connection") the first time you visit -- that's expected
for a self-signed, local-only certificate; click through it (e.g.
"Advanced" -> "Proceed to localhost").

`ft.run(..., export_asgi_app=True)` hands back a plain FastAPI app with
the Flet frontend mounted on it, instead of `ft.run` starting its own
(plain-HTTP-only) server -- that ASGI app is then served directly via
`uvicorn.run(..., ssl_certfile=..., ssl_keyfile=...)`, which is the only
place TLS termination can actually be configured.

Port is configurable via the CODING_ADVENTURE_WEB_PORT environment
variable (default 8550) -- see run_app_web_ui.bat/.sh, or set it yourself
before running this directly."""
from __future__ import annotations

import os
import threading
import webbrowser

import flet as ft
import uvicorn

from app.config.ssl_cert import ensure_self_signed_certificate
from app.ui.app_window import main

PORT = int(os.environ.get("CODING_ADVENTURE_WEB_PORT", "8550"))

app = ft.run(main, export_asgi_app=True)


def _open_browser_shortly_after_startup() -> None:
    """`uvicorn.run()` blocks the main thread until the server is
    listening, so opening the browser has to happen from a second thread
    -- delayed slightly so it doesn't race the server actually binding
    the port."""
    threading.Timer(1.0, lambda: webbrowser.open(f"https://localhost:{PORT}")).start()


if __name__ == "__main__":
    cert_path, key_path = ensure_self_signed_certificate()
    _open_browser_shortly_after_startup()
    uvicorn.run(
        app,
        host="localhost",
        port=PORT,
        ssl_certfile=cert_path,
        ssl_keyfile=key_path,
    )
