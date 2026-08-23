"""Translates raw interpreter/compiler output into concise, professional
explanations. Raw text stays available on request in the UI."""
from __future__ import annotations

import re
from typing import Optional

PYTHON_FRIENDLY: dict[str, tuple[str, str]] = {
    "SyntaxError": ("Syntax error.", "Check for a missing colon, parenthesis, or quote."),
    "IndentationError": ("Indentation error.", "Python is whitespace-sensitive -- check your indent levels."),
    "TabError": ("Inconsistent tabs/spaces.", "Stick to one or the other, not both, in the same block."),
    "NameError": ("Undefined name.", "Check the spelling, or that it's assigned before use."),
    "TypeError": ("Type mismatch.", "Check the types being combined or passed to a call."),
    "AttributeError": ("Missing attribute.", "Check the object actually has that attribute/method."),
    "ZeroDivisionError": ("Division by zero.", "Guard the denominator before dividing."),
    "ImportError": ("Import failed.", "Check the module name and that it's installed."),
    "ModuleNotFoundError": ("Module not found.", "Check the module name and that it's installed."),
    "IndexError": ("Index out of range.", "Check the sequence length before indexing."),
    "KeyError": ("Key not found.", "Check the key exists, or use .get() with a default."),
    "ValueError": ("Invalid value.", "Check the value matches what's expected here."),
    "EOFError": ("Input expected but not provided.", "Fill in the input box, then run again."),
    "RecursionError": ("Recursion too deep.", "Check the base case actually stops the recursion."),
}

DEFAULT_MESSAGE = "Something went wrong while running this code."
DEFAULT_HINT = "Check the details below and try again."

_CODE_FRAME_RE = re.compile(r'File "<exercise>", line (\d+)')


def translate_error(stderr: str, language: str = "python") -> tuple[str, str]:
    if language == "python":
        exc_type = _last_exception_type(stderr)
        return PYTHON_FRIENDLY.get(exc_type, (DEFAULT_MESSAGE, DEFAULT_HINT))
    return (DEFAULT_MESSAGE, DEFAULT_HINT)


def _last_exception_type(stderr: str) -> str:
    for line in reversed(stderr.strip().splitlines()):
        line = line.strip()
        if line:
            return line.split(":", 1)[0].strip()
    return ""


def extract_error_line_number(stderr: str) -> Optional[int]:
    matches = _CODE_FRAME_RE.findall(stderr)
    return int(matches[-1]) if matches else None
