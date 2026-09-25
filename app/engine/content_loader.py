"""Shared YAML loading for exercise and quiz content.

Two things every content loader needs and neither should reinvent:

- the fastest available YAML parser (`CSafeLoader` when libyaml is
  present -- roughly 5-10x faster than the pure-Python SafeLoader, which
  matters when a track has 400+ files), with a safe fallback;
- a load error that names the file. `Exercise(**data)` with a misspelled
  key raises `TypeError: unexpected keyword argument 'hnits'` -- true,
  but useless without knowing which of 455 files to open."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


class ContentError(ValueError):
    """A content file is malformed. Always carries the offending path."""

    def __init__(self, path: Path, message: str) -> None:
        self.path = path
        super().__init__(f"{path}: {message}")


def load_yaml_file(path: Path) -> Any:
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=_LOADER)
    except yaml.YAMLError as exc:
        raise ContentError(path, f"invalid YAML -- {exc}") from exc


def build_model(model_cls: type, data: Any, path: Path):
    """Instantiate a content dataclass from a YAML mapping, converting the
    stdlib's unhelpful TypeError/ValueError into a ContentError that says
    which file to fix."""
    if not isinstance(data, dict):
        raise ContentError(path, f"expected a mapping at the top level, got {type(data).__name__}")
    try:
        return model_cls(**data)
    except TypeError as exc:
        # "__init__() got an unexpected keyword argument 'x'" or a missing
        # required field -- both are authoring mistakes.
        raise ContentError(path, f"{model_cls.__name__} could not be built -- {exc}") from exc
    except ValueError as exc:
        raise ContentError(path, str(exc)) from exc
