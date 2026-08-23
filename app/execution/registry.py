"""Maps a language key to its ExecutionEngine instance."""
from __future__ import annotations

from app.execution.base import ExecutionEngine
from app.execution.cpp_engine import CppEngine
from app.execution.java_engine import JavaEngine
from app.execution.python_engine import PythonEngine
from app.execution.spring_engine import SpringEngine

_ENGINES: dict[str, ExecutionEngine] = {
    "python": PythonEngine(),
    "java": JavaEngine(),
    "cpp": CppEngine(),
    "spring": SpringEngine(),
}


def get_engine(language: str) -> ExecutionEngine:
    if language not in _ENGINES:
        raise ValueError(f"No execution engine registered for language '{language}'")
    return _ENGINES[language]
