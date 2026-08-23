"""Detects whether a language track's real local toolchain is on PATH.

Used by the language picker / track hub to show an honest "toolchain not
found, here's how to install it" message instead of a confusing failure
the first time someone tries to run an exercise."""
from __future__ import annotations

import shutil
from dataclasses import dataclass


@dataclass(frozen=True)
class ToolchainStatus:
    available: bool
    missing: list[str]
    install_hint: str


_REQUIREMENTS: dict[str, tuple[list[str], str]] = {
    "python": ([], "Bundled with this app -- nothing to install."),
    "java": (
        ["javac", "java"],
        "Install a JDK (e.g. Eclipse Temurin) from https://adoptium.net and ensure javac/java are on PATH.",
    ),
    "cpp": (
        ["g++"],
        "Install a C++ toolchain (e.g. MinGW-w64 or MSYS2's mingw-w64-gcc) and ensure g++ is on PATH.",
    ),
    "spring": (
        ["mvn", "java"],
        "Install a JDK and Maven, and ensure mvn/java are on PATH.",
    ),
}


def check_toolchain(language: str) -> ToolchainStatus:
    tools, hint = _REQUIREMENTS.get(language, ([], ""))
    missing = [tool for tool in tools if shutil.which(tool) is None]
    return ToolchainStatus(available=not missing, missing=missing, install_hint=hint)
