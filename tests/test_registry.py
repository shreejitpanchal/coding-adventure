import pytest

from app.execution import registry
from app.execution.base import ExecutionEngine
from app.execution.python_engine import PythonEngine
from app.execution.python_inprocess_engine import PythonInProcessEngine
from app.execution.registry import ENGINE_FACTORIES, create_engine, has_engine


def test_every_registered_language_builds_an_engine():
    for language in ENGINE_FACTORIES:
        engine = create_engine(language)
        assert isinstance(engine, ExecutionEngine)


def test_each_call_is_a_fresh_instance():
    assert create_engine("java") is not create_engine("java")


def test_ai_runs_on_the_python_engine_class():
    assert type(create_engine("ai")) is type(create_engine("python"))


def test_architecture_has_no_engine_on_purpose():
    assert not has_engine("architecture")


def test_unknown_language_error_names_the_known_keys():
    with pytest.raises(ValueError, match="cobol") as excinfo:
        create_engine("cobol")
    assert "python" in str(excinfo.value)


def test_python_swaps_to_in_process_engine_on_android(monkeypatch):
    monkeypatch.setattr(registry, "is_android", lambda: True)
    assert isinstance(create_engine("python"), PythonInProcessEngine)
    monkeypatch.setattr(registry, "is_android", lambda: False)
    assert isinstance(create_engine("python"), PythonEngine)
