"""Java source helpers shared by the Java and Spring engines."""
from __future__ import annotations

import re

_PUBLIC_CLASS_RE = re.compile(r"\bpublic\s+(?:final\s+|abstract\s+)?class\s+(\w+)")
_ANY_CLASS_RE = re.compile(r"\bclass\s+(\w+)")


def detect_class_name(code: str, default: str = "Solution") -> str:
    """The class the file must be named after: the `public class`, else
    the first `class` declared, else `default`."""
    match = _PUBLIC_CLASS_RE.search(code) or _ANY_CLASS_RE.search(code)
    return match.group(1) if match else default
