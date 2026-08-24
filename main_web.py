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
before running this directly.

On Windows, closing the browser tab (or the browser itself) while a
WebSocket/HTTPS connection is still open makes the OS reset that
connection instead of closing it cleanly -- asyncio's default
ProactorEventLoop then logs a harmless but noisy
"ConnectionResetError: [WinError 10054]" traceback for it (a
long-standing CPython issue, bpo-39232, not specific to this app or a
sign anything actually broke). `_silence_proactor_connection_reset()`
below applies the standard, widely-used workaround: wrapping the
transport teardown callback that raises it so the exception is
swallowed rather than logged, without changing any actual shutdown
behavior."""
from __future__ import annotations

import os
import sys
import threading
import webbrowser

import flet as ft
import uvicorn

from app.config.ssl_cert import ensure_self_signed_certificate
from app.ui.app_window import main

PORT = int(os.environ.get("CODING_ADVENTURE_WEB_PORT", "8550"))

app = ft.run(main, export_asgi_app=True)


def _silence_proactor_connection_reset() -> None:
    if sys.platform != "win32":
        return

    from asyncio.proactor_events import _ProactorBasePipeTransport

    original = _ProactorBasePipeTransport._call_connection_lost

    def _call_connection_lost_quietly(self, exc):
        try:
            original(self, exc)
        except ConnectionResetError:
            pass

    _ProactorBasePipeTransport._call_connection_lost = _call_connection_lost_quietly


def _open_browser_shortly_after_startup() -> None:
    """`uvicorn.run()` blocks the main thread until the server is
    listening, so opening the browser has to happen from a second thread
    -- delayed slightly so it doesn't race the server actually binding
    the port. Marked daemon so it can never keep the process alive on
    its own (it finishes within ~1s regardless, but this is the correct
    default for a fire-and-forget background thread either way)."""
    timer = threading.Timer(1.0, lambda: webbrowser.open(f"https://localhost:{PORT}"))
    timer.daemon = True
    timer.start()


if __name__ == "__main__":
    _silence_proactor_connection_reset()
    cert_path, key_path = ensure_self_signed_certificate()
    _open_browser_shortly_after_startup()
    try:
        uvicorn.run(
            app,
            host="localhost",
            port=PORT,
            ssl_certfile=cert_path,
            ssl_keyfile=key_path,
        )
    except KeyboardInterrupt:
        pass
    print("Stopped.")
