"""Display metadata (title, icon, color) for exercise categories, used by
the topic browser. Purely presentational -- adding a category here isn't
required for the engine to work (ExerciseEngine.categories() derives the
actual set from content), but a category without an entry here falls back
to a generic label/color in the UI."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryMeta:
    title: str
    icon: str
    color: str


CATEGORY_META: dict[str, CategoryMeta] = {
    "idioms_gotchas": CategoryMeta("Idioms & Gotchas", "\U0001F9E0", "#7C9EFF"),
    "core_refresher": CategoryMeta("Core Language Refresher", "\U0001F527", "#4ADE9E"),
    "data_structures": CategoryMeta("Data Structures & Algorithms", "\U0001F5C2️", "#FFC857"),
    "stdlib_deep_dive": CategoryMeta("Standard Library Deep Dive", "\U0001F4DA", "#5DE8FF"),
    "concurrency_async": CategoryMeta("Concurrency & Async", "⚡", "#FF8A5B"),
    "thread_scheduling": CategoryMeta("Thread Scheduling", "\U0001F9F5", "#C77DFF"),
    "sync_vs_async": CategoryMeta("Sync vs Async", "\U0001F504", "#3BC5DD"),
    "functional_programming": CategoryMeta("Functional Programming", "\U0001F3AF", "#4ADE9E"),
    "recursion": CategoryMeta("Recursion", "\U0001F501", "#F97316"),
    "dependency_management": CategoryMeta("Dependency Management", "\U0001F4E6", "#94A3B8"),
    "packaging": CategoryMeta("Packaging", "\U0001F4E4", "#EAB308"),
    "deployment": CategoryMeta("Deployment", "\U0001F680", "#22D3EE"),
    "observability": CategoryMeta("Observability", "\U0001F50D", "#A78BFA"),
    "gotcha_gauntlet": CategoryMeta("Gotcha Gauntlet", "\U0001F41E", "#FF6B6B"),
    "dependency_injection": CategoryMeta("Dependency Injection", "\U0001F9E9", "#7C9EFF"),
    "bean_lifecycle": CategoryMeta("Bean Lifecycle & Scopes", "\U0001F331", "#4ADE9E"),
    "configuration_profiles": CategoryMeta("Configuration & Profiles", "\U0001F39B️", "#FFC857"),
    "events": CategoryMeta("Application Events", "\U0001F4E3", "#5DE8FF"),
    "aop": CategoryMeta("Aspect-Oriented Programming", "\U0001F578️", "#FF8A5B"),
    "resilience": CategoryMeta("Resilience Patterns", "\U0001F6E1️", "#F97316"),
}

DEFAULT_META = CategoryMeta("More Practice", "⭐", "#8A93C7")

# Categories that make up the flagship "find-the-bug" debug puzzle track --
# called out on its own card in the track hub, not lumped into the plain
# topic browser.
GOTCHA_CATEGORY = "gotcha_gauntlet"


def get_category_meta(category: str) -> CategoryMeta:
    return CATEGORY_META.get(category, DEFAULT_META)
