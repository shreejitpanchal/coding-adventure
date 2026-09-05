"""Detects whether a language track's real local toolchain is on PATH.

Used by the language picker / track hub to show an honest "toolchain not
found, here's how to install it" message instead of a confusing failure
the first time someone tries to run an exercise."""
from __future__ import annotations

import platform
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
    "node": (
        ["node"],
        "Install Node.js LTS from https://nodejs.org and ensure node is on PATH.",
    ),
    "ai": ([], "Bundled with this app -- runs on the same Python interpreter as the Python track."),
    "architecture": ([], "No toolchain needed -- purely conceptual, no code runs for this track."),
}


def check_toolchain(language: str) -> ToolchainStatus:
    tools, hint = _REQUIREMENTS.get(language, ([], ""))
    missing = [tool for tool in tools if shutil.which(tool) is None]
    return ToolchainStatus(available=not missing, missing=missing, install_hint=hint)


# Longer, step-by-step guides for the language picker's "Toolchain needed"
# dialog -- keyed by platform.system()'s own values ("Windows", "Darwin",
# "Linux"). ToolchainStatus.install_hint stays a short one-liner (it's also
# reused verbatim inside ExecutionResult.blocked_message, where a multi-step
# guide would be out of place), so this is a separate, richer lookup used
# only by the UI.
_INSTALL_GUIDES: dict[str, dict[str, list[str]]] = {
    "java": {
        "Windows": [
            "Open PowerShell or Command Prompt.",
            "Run: winget install EclipseAdoptium.Temurin.21.JDK",
            "(No winget? Download the installer instead from https://adoptium.net)",
            "Close and reopen your terminal, VS Code, and this app afterward -- "
            "Windows doesn't push a PATH change into programs that are already running.",
        ],
        "Darwin": [
            "Install Homebrew first if you don't have it yet: https://brew.sh",
            "Run: brew install openjdk",
            "Follow the PATH-linking command brew prints after installing.",
            "Open a new terminal window so the PATH change takes effect.",
        ],
        "Linux": [
            "Debian/Ubuntu: sudo apt update && sudo apt install default-jdk",
            "Fedora: sudo dnf install java-latest-openjdk-devel",
            "Arch: sudo pacman -S jdk-openjdk",
        ],
    },
    "cpp": {
        "Windows": [
            "Open PowerShell or Command Prompt.",
            "Run: winget install MSYS2.MSYS2",
            "Open the \"MSYS2 MinGW64\" shortcut from the Start menu (not a regular terminal).",
            "In that MSYS2 shell, run: pacman -S mingw-w64-x86_64-gcc",
            "Add C:\\msys64\\mingw64\\bin to your PATH (Windows Settings -> "
            "\"Edit environment variables for your account\").",
            "Close and reopen your terminal, VS Code, and this app afterward -- "
            "Windows doesn't push a PATH change into programs that are already running.",
        ],
        "Darwin": [
            "Install the Xcode Command Line Tools: xcode-select --install",
            "That provides clang, which g++ is aliased to on macOS -- no extra install needed.",
            "Open a new terminal window afterward so the change takes effect.",
        ],
        "Linux": [
            "Debian/Ubuntu: sudo apt update && sudo apt install build-essential",
            "Fedora: sudo dnf groupinstall \"Development Tools\"",
            "Arch: sudo pacman -S base-devel",
        ],
    },
    "spring": {
        "Windows": [
            "Open PowerShell or Command Prompt.",
            "Run: winget install EclipseAdoptium.Temurin.21.JDK",
            "Run: winget install Apache.Maven",
            "Close and reopen your terminal, VS Code, and this app afterward -- "
            "Windows doesn't push a PATH change into programs that are already running.",
        ],
        "Darwin": [
            "Install Homebrew first if you don't have it yet: https://brew.sh",
            "Run: brew install openjdk maven",
            "Follow the PATH-linking command brew prints for openjdk.",
            "Open a new terminal window so the PATH change takes effect.",
        ],
        "Linux": [
            "Debian/Ubuntu: sudo apt update && sudo apt install default-jdk maven",
            "Fedora: sudo dnf install java-latest-openjdk-devel maven",
            "Arch: sudo pacman -S jdk-openjdk maven",
        ],
    },
    "node": {
        "Windows": [
            "Open PowerShell or Command Prompt.",
            "Run: winget install OpenJS.NodeJS.LTS",
            "Close and reopen your terminal, VS Code, and this app afterward -- "
            "Windows doesn't push a PATH change into programs that are already running.",
        ],
        "Darwin": [
            "Install Homebrew first if you don't have it yet: https://brew.sh",
            "Run: brew install node",
            "Open a new terminal window so the PATH change takes effect.",
        ],
        "Linux": [
            "Debian/Ubuntu: sudo apt update && sudo apt install nodejs npm",
            "Fedora: sudo dnf install nodejs",
            "Arch: sudo pacman -S nodejs npm",
        ],
    },
}

_VERIFY_COMMANDS: dict[str, str] = {
    "java": "javac -version",
    "cpp": "g++ --version",
    "spring": "mvn -version",
    "node": "node --version",
}


def get_install_guide(language: str) -> tuple[list[str], str] | None:
    """Returns (ordered_steps, verify_command) for the current OS, or None
    if this language has no toolchain to install (e.g. Python) or isn't
    recognized."""
    guides = _INSTALL_GUIDES.get(language)
    if not guides:
        return None
    os_name = platform.system()
    steps = guides.get(os_name) or next(iter(guides.values()))
    return steps, _VERIFY_COMMANDS.get(language, "")
