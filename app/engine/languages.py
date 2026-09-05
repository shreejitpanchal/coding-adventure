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
        tagline="Dependency injection, bean lifecycle, and configuration -- keep your instincts sharp.",
        available=True,
    ),
    "node": LanguageInfo(
        key="node", title="Node.js", icon="\U0001F7E2",
        tagline="Event loop gotchas, async/await, and idiomatic modern JavaScript -- keep your instincts sharp.",
        available=True,
    ),
    "ai": LanguageInfo(
        key="ai", title="AI", icon="\U0001F916",
        tagline="ML fundamentals, RAG, agentic frameworks, and MCP -- hand-rolled, dependency-free Python.",
        available=True,
    ),
    "architecture": LanguageInfo(
        key="architecture", title="Architecture", icon="\U0001F3D7️",
        tagline="Event-driven design, microservices, CQRS, and modern system-design principles -- conceptual, no code to run.",
        available=True,
    ),
}

LANGUAGE_ORDER = ["python", "java", "cpp", "spring", "node", "ai", "architecture"]


def get_language(key: str) -> LanguageInfo:
    return LANGUAGES.get(key, LANGUAGES["python"])
