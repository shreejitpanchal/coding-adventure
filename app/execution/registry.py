"""Maps a language key to the ExecutionEngine class that runs it.

Deliberately holds no instances: `create_engine()` builds one on demand
and the caller (AppState.execution_engine()) owns and caches it, the same
way it already owns the per-language ExerciseEngine/QuizEngine. Keeping
the registry instance-free means the app has no module-level singletons
to reach for, nothing is constructed for tracks the user never opens, and
tests can build an engine without touching shared state.

On Android, PythonEngine's subprocess.Popen approach can't work at all --
a non-rooted app can't spawn a sibling OS process there -- so Python
swaps to the in-process engine specifically on that platform. Java/C++/
Spring/Node have no equivalent: they need a real javac/g++/mvn/node
toolchain that doesn't exist on Android and can't be bundled into an app
sandbox, so they're left as their normal (subprocess) engines, which
simply never find their toolchain there -- see toolchain_check.py and
language_select.py for how that's surfaced to the user instead of
crashing.

"ai" (ML/RAG/agentic frameworks/MCP) is its own top-level track for
progress/XP/streak purposes, but its content is plain, dependency-free
Python -- it runs on the same engine class as the python track, not a
separate implementation. "architecture" has no entry at all: every one
of its exercises is requires_code=False, so nothing ever asks for its
engine.
"""
from __future__ import annotations

from typing import Callable

from app.execution.android_platform import is_android
from app.execution.base import ExecutionEngine
from app.execution.cpp_engine import CppEngine
from app.execution.java_engine import JavaEngine
from app.execution.node_engine import NodeEngine
from app.execution.python_engine import PythonEngine
from app.execution.python_inprocess_engine import PythonInProcessEngine
from app.execution.spring_engine import SpringEngine


def _python_engine() -> ExecutionEngine:
    return PythonInProcessEngine() if is_android() else PythonEngine()


ENGINE_FACTORIES: dict[str, Callable[[], ExecutionEngine]] = {
    "python": _python_engine,
    "ai": _python_engine,
    "java": JavaEngine,
    "cpp": CppEngine,
    "spring": SpringEngine,
    "node": NodeEngine,
}


def has_engine(language: str) -> bool:
    return language in ENGINE_FACTORIES


def create_engine(language: str) -> ExecutionEngine:
    """A fresh engine for `language`. Raises with the list of known keys
    for anything unregistered -- a misconfigured track should fail loud at
    the first Run, not silently execute nothing."""
    try:
        factory = ENGINE_FACTORIES[language]
    except KeyError:
        raise ValueError(
            f"No execution engine registered for language {language!r}. "
            f"Known: {sorted(ENGINE_FACTORIES)}. Add a factory to app/execution/registry.py "
            f"or mark the track's exercises requires_code: false."
        ) from None
    return factory()
