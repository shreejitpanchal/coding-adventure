"""Cooperative timeout mechanism for PythonInProcessEngine (Android).

A subprocess-based engine cancels a runaway loop with `process.kill()` --
the OS tears down the whole child process, loop and all. Code run
in-process (exec()'d in the same process as the app itself, which is
what Android's app-sandboxing forces, since a non-rooted app can't spawn
a sibling OS process the way subprocess.Popen does on desktop/web) has no
such OS-level kill switch available. Instead, an AST transform below
inserts a call to a watchdog's tick() at the top of every for/while loop
body. tick() is cheap on its own and only checks the wall clock every
CHECK_INTERVAL calls, so it stays negligible even inside a tight,
multi-million-iteration loop -- but the cancellation flag is checked on
every single call, so a user-requested Stop is still picked up promptly.

Ported from python-adventure-kids' app/sandbox/watchdog.py (same
underlying problem: no OS process to kill on Android), with its
AST-based builtins/import safety layer deliberately left behind --
this app has no adversarial threat model to defend against (see
app/execution/base.py's docstring), so only the loop-cancellation
mechanism itself needed porting, not the kid-safety sandbox built
around it there.

Known, accepted limitation: a single expensive operation with no loop or
function call at all (e.g. 10**10**10**10) can't be interrupted by any
pure-Python cooperative mechanism, including this one. Acceptable for
curated lesson content; not solved here.
"""
from __future__ import annotations

import ast
import threading
import time

CHECK_INTERVAL = 200
TICK_FUNC_NAME = "__codingadventure_tick__"


class WatchdogTimeout(BaseException):
    """Raised inside exec()'d code when it runs past its deadline or is
    cancelled. Subclasses BaseException (not Exception) so a broad
    `except Exception` -- or a bare `except: pass` -- in the submitted
    code can't accidentally catch and swallow it."""


class Watchdog:
    def __init__(self, timeout: float) -> None:
        self._deadline = time.monotonic() + timeout
        self._cancelled = threading.Event()
        self._count = 0

    def cancel(self) -> None:
        self._cancelled.set()

    def tick(self) -> None:
        if self._cancelled.is_set():
            raise WatchdogTimeout()
        self._count += 1
        if self._count % CHECK_INTERVAL == 0 and time.monotonic() >= self._deadline:
            raise WatchdogTimeout()


class _LoopTickInjector(ast.NodeTransformer):
    """Inserts a call to __codingadventure_tick__() as the first statement
    in every for/while loop body.

    The injected call reuses the loop statement's own line number (via
    ast.copy_location) rather than introducing a new one, so line numbers
    reported in tracebacks for the rest of the submitted code stay
    accurate.
    """

    def visit_For(self, node: ast.For) -> ast.For:
        self.generic_visit(node)
        node.body.insert(0, self._tick_statement(node))
        return node

    def visit_While(self, node: ast.While) -> ast.While:
        self.generic_visit(node)
        node.body.insert(0, self._tick_statement(node))
        return node

    @staticmethod
    def _tick_statement(node: ast.AST) -> ast.Expr:
        tick = ast.Expr(
            value=ast.Call(func=ast.Name(id=TICK_FUNC_NAME, ctx=ast.Load()), args=[], keywords=[])
        )
        ast.copy_location(tick, node)
        ast.fix_missing_locations(tick)
        return tick


def compile_with_watchdog(source: str, filename: str = "<exercise>"):
    """Parses source, injects watchdog ticks into every loop, and compiles
    the result. Raises SyntaxError directly if source doesn't parse --
    callers should let that propagate."""
    tree = ast.parse(source, filename=filename)
    tree = _LoopTickInjector().visit(tree)
    ast.fix_missing_locations(tree)
    return compile(tree, filename=filename, mode="exec", optimize=0)
