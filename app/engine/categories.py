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
    "gotcha_gauntlet": CategoryMeta("Gotcha Gauntlet", "\U0001F41E", "#FF6B6B"),
}

DEFAULT_META = CategoryMeta("More Practice", "⭐", "#8A93C7")

# Categories that make up the flagship "find-the-bug" debug puzzle track --
# called out on its own card in the track hub, not lumped into the plain
# topic browser.
GOTCHA_CATEGORY = "gotcha_gauntlet"


def get_category_meta(category: str) -> CategoryMeta:
    return CATEGORY_META.get(category, DEFAULT_META)
