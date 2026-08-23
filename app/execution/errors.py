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

JAVA_FRIENDLY: dict[str, tuple[str, str]] = {
    "NullPointerException": ("Null reference.", "Check that the object isn't null before calling a method or field on it."),
    "ArrayIndexOutOfBoundsException": ("Array index out of range.", "Check the array's length before indexing into it."),
    "IndexOutOfBoundsException": ("Index out of range.", "Check the index is within bounds for this collection."),
    "ArithmeticException": ("Arithmetic error.", "Check for division by zero."),
    "ClassCastException": ("Invalid cast.", "Check the object's actual runtime type before casting it."),
    "NumberFormatException": ("Invalid number format.", "Check the string actually contains a valid number before parsing it."),
    "StackOverflowError": ("Stack overflow.", "Check the recursion has a base case that actually stops it."),
    "IllegalArgumentException": ("Illegal argument.", "Check the value passed in matches what the method expects."),
    "IllegalStateException": ("Illegal state.", "Check the object is in the right state before calling this."),
    "ConcurrentModificationException": ("Collection modified during iteration.", "Iterate over a copy, use removeIf(), or use an Iterator's own remove() instead of mutating the collection directly."),
    "UnsupportedOperationException": ("Unsupported operation.", "Check whether this collection is immutable/fixed-size before mutating it."),
    "NoSuchElementException": ("No element found.", "Check the collection/iterator actually has an element before reading it."),
}

DEFAULT_MESSAGE = "Something went wrong while running this code."
DEFAULT_HINT = "Check the details below and try again."

_PYTHON_CODE_FRAME_RE = re.compile(r'File "<exercise>", line (\d+)')
_JAVA_LINE_RE = re.compile(r"\.java:(\d+)")
_JAVA_EXCEPTION_RE = re.compile(r'Exception in thread "\w+" (?:[\w.]+\.)?(\w+(?:Exception|Error))')
_JAVA_COMPILE_ERROR_RE = re.compile(r":\d+: error:")


def translate_error(stderr: str, language: str = "python") -> tuple[str, str]:
    if language == "python":
        exc_type = _last_exception_type(stderr)
        return PYTHON_FRIENDLY.get(exc_type, (DEFAULT_MESSAGE, DEFAULT_HINT))
    if language == "java":
        return _translate_java_error(stderr)
    return (DEFAULT_MESSAGE, DEFAULT_HINT)


def _last_exception_type(stderr: str) -> str:
    for line in reversed(stderr.strip().splitlines()):
        line = line.strip()
        if line:
            return line.split(":", 1)[0].strip()
    return ""


def _translate_java_error(stderr: str) -> tuple[str, str]:
    if _JAVA_COMPILE_ERROR_RE.search(stderr):
        return ("Compile error.", "Check the line the compiler points to for a missing semicolon, brace, or type mismatch.")
    match = _JAVA_EXCEPTION_RE.search(stderr)
    exc_type = match.group(1) if match else ""
    return JAVA_FRIENDLY.get(exc_type, (DEFAULT_MESSAGE, DEFAULT_HINT))


def extract_error_line_number(stderr: str, language: str = "python") -> Optional[int]:
    pattern = _JAVA_LINE_RE if language == "java" else _PYTHON_CODE_FRAME_RE
    matches = pattern.findall(stderr)
    return int(matches[-1]) if matches else None
