"""The set of language tracks the app knows about, and which ones have real
content/execution behind them yet. Purely descriptive -- adding a language
here doesn't build the track, it just makes it selectable (and, if not yet
`available`, shown as "Coming soon" on the language picker)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageInfo:
    key: str
    title: str
    icon: str
    tagline: str
    available: bool
    """False renders the card as locked/"coming soon" on the language
    picker -- content and an execution engine exist only for `available`
    tracks. Not derived from toolchain detection: a track can be built out
    in content but still show a friendly toolchain-missing message per
    exercise (see app.execution.toolchain_check)."""


LANGUAGES: dict[str, LanguageInfo] = {
    "python": LanguageInfo(
        key="python", title="Python", icon="\U0001F40D",
        tagline="Idioms, gotchas, stdlib depth, and concurrency -- keep your instincts sharp.",
        available=True,
    ),
    "java": LanguageInfo(
        key="java", title="Java", icon="☕",
        tagline="Idioms, streams, the Collections Framework, and concurrency -- keep your instincts sharp.",
        available=True,
    ),
    "cpp": LanguageInfo(
        key="cpp", title="C++", icon="⚙️",
        tagline="Idioms, modern STL, RAII, and concurrency -- keep your instincts sharp.",
        available=True,
    ),
    "spring": LanguageInfo(
        key="spring", title="Spring", icon="\U0001F343",
        tagline="Coming soon -- Spring Boot, DI, and REST refreshers.",
        available=False,
    ),
}

LANGUAGE_ORDER = ["python", "java", "cpp", "spring"]


def get_language(key: str) -> LanguageInfo:
    return LANGUAGES.get(key, LANGUAGES["python"])
