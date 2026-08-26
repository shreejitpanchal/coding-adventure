"""Maps a language key to its ExecutionEngine instance."""
from __future__ import annotations

from app.execution.android_platform import is_android
from app.execution.base import ExecutionEngine
from app.execution.cpp_engine import CppEngine
from app.execution.java_engine import JavaEngine
from app.execution.node_engine import NodeEngine
from app.execution.python_engine import PythonEngine
from app.execution.python_inprocess_engine import PythonInProcessEngine
from app.execution.spring_engine import SpringEngine

# On Android, PythonEngine's subprocess.Popen approach can't work at all --
# a non-rooted app can't spawn a sibling OS process there -- so Python
# swaps to the in-process engine specifically on that platform. Java/C++/
# Spring have no equivalent: they need a real javac/g++/mvn toolchain that
# doesn't exist on Android and can't be bundled into an app sandbox, so
# they're left as their normal (subprocess) engines, which simply never
# find their toolchain there -- see toolchain_check.py and
# language_select.py for how that's surfaced to the user instead of
# crashing.
_ENGINES: dict[str, ExecutionEngine] = {
    "python": PythonInProcessEngine() if is_android() else PythonEngine(),
    "java": JavaEngine(),
    "cpp": CppEngine(),
    "spring": SpringEngine(),
    "node": NodeEngine(),
}


def get_engine(language: str) -> ExecutionEngine:
    if language not in _ENGINES:
        raise ValueError(f"No execution engine registered for language '{language}'")
    return _ENGINES[language]
