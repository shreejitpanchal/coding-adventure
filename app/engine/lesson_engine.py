"""Loads one language track's exercises from YAML, kept separate from
application code -- adding or changing an exercise never requires touching
app code, just a YAML file under content/<language>/lessons/."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from app.config.platform_paths import resolve_platform_data_dir
from app.engine.exercise import Exercise
from app.execution.android_platform import is_android

CONTENT_ROOT = Path(__file__).resolve().parent.parent.parent / "content"

# User-added exercises live outside the git checkout entirely, so they
# survive a `git pull` (which would otherwise never touch them, but also
# never risks clobbering a built-in file the user copied and edited in
# place). Loaded strictly AFTER built-in content -- see _load().
CUSTOM_CONTENT_DIRNAME = "custom"

# On Android, Java/C++/Spring/Node can never actually run (no javac/g++/
# mvn/node on the device), so a user there can never legitimately
# "complete" an exercise to unlock the next category_level -- normal
# completion-gated progression would permanently lock almost all of this
# content. Python is excluded since it genuinely runs there via the
# in-process engine.
MOBILE_ALWAYS_UNLOCKED_LANGUAGES = {"java", "cpp", "spring", "node"}

# These two tracks are unconditionally unlocked, on every platform, by
# product decision -- unlike every other track, where completion-gated
# progression is the point. `architecture` is a reference-style library of
# independent conceptual topics with no code to run at all (requires_code
# is False on every exercise), so there's no reason to force a specific
# reading order; `ai` was made unlocked the same way at the user's request.
ALWAYS_UNLOCKED_LANGUAGES = {"architecture", "ai"}


class ExerciseEngine:
    def __init__(
        self, language: str, content_dir: Optional[Path] = None, custom_content_dir: Optional[Path] = None,
    ):
        self.language = language
        self.content_dir = content_dir or (CONTENT_ROOT / language / "lessons")
        self.custom_content_dir = custom_content_dir or (
            resolve_platform_data_dir() / CUSTOM_CONTENT_DIRNAME / language / "lessons"
        )
        self._exercises: dict[str, Exercise] = {}
        self._order: list[str] = []
        self._load()

    def _load(self) -> None:
        exercises: list[Exercise] = []
        seen_paths: dict[str, Path] = {}
        # Built-in content first, then the user's custom overlay -- loaded
        # in that fixed order so a duplicate id always fails loud (below)
        # rather than one silently shadowing the other depending on
        # directory iteration order.
        for directory in (self.content_dir, self.custom_content_dir):
            if not directory.is_dir():
                continue
            for path in sorted(directory.glob("*.yaml")):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                if not data:
                    continue
                data.setdefault("language", self.language)
                exercise = Exercise(**data)
                if exercise.id in seen_paths:
                    raise ValueError(
                        f"Duplicate exercise id {exercise.id!r}: already loaded from "
                        f"{seen_paths[exercise.id]}, also found in {path}. Exercise ids "
                        f"must be unique across both built-in and custom content."
                    )
                seen_paths[exercise.id] = path
                exercises.append(exercise)
        exercises.sort(key=lambda ex: ex.level)
        self._exercises = {ex.id: ex for ex in exercises}
        self._order = [ex.id for ex in exercises]

    def __len__(self) -> int:
        return len(self._order)

    def get(self, exercise_id: str) -> Optional[Exercise]:
        return self._exercises.get(exercise_id)

    def has(self, exercise_id: str) -> bool:
        return exercise_id in self._exercises

    def all_in_order(self) -> list[Exercise]:
        return [self._exercises[eid] for eid in self._order]

    def categories(self) -> list[str]:
        seen: list[str] = []
        for ex in self.all_in_order():
            if ex.category not in seen:
                seen.append(ex.category)
        return seen

    def lessons_in_category(self, category: str) -> list[Exercise]:
        return sorted(
            (ex for ex in self._exercises.values() if ex.category == category),
            key=lambda ex: ex.category_level,
        )

    def is_unlocked(self, exercise: Exercise, completed_ids: set[str]) -> bool:
        if self.language in ALWAYS_UNLOCKED_LANGUAGES:
            return True
        if self.language in MOBILE_ALWAYS_UNLOCKED_LANGUAGES and is_android():
            return True
        if exercise.category_level <= 1:
            return True
        earlier = [
            ex for ex in self.lessons_in_category(exercise.category)
            if ex.category_level < exercise.category_level
        ]
        return all(ex.id in completed_ids for ex in earlier)

    def next_unlocked_in_category(self, category: str, completed_ids: set[str]) -> Optional[Exercise]:
        for ex in self.lessons_in_category(category):
            if ex.id not in completed_ids and self.is_unlocked(ex, completed_ids):
                return ex
        return None

    def category_completion(self) -> dict[str, tuple[int, int]]:
        """category -> (done, total), done computed by the caller passing
        completed_ids in via category_completion_for()."""
        return {cat: (0, len(self.lessons_in_category(cat))) for cat in self.categories()}

    def category_completion_for(self, completed_ids: set[str]) -> dict[str, tuple[int, int]]:
        result: dict[str, tuple[int, int]] = {}
        for cat in self.categories():
            items = self.lessons_in_category(cat)
            done = sum(1 for ex in items if ex.id in completed_ids)
            result[cat] = (done, len(items))
        return result

    def daily_refresher(self, completed_ids: set[str], count: int = 5) -> list[Exercise]:
        """A small guided set for "today's refresher" -- round-robins the
        next unlocked, incomplete exercise from each category until `count`
        is reached, so a daily session naturally spans topics instead of
        grinding one category at a time."""
        completed = set(completed_ids)
        picks: list[Exercise] = []
        categories = self.categories()
        if not categories:
            return picks
        cursor: dict[str, int] = {cat: 0 for cat in categories}
        guard = 0
        while len(picks) < count and guard < count * len(categories) + len(categories):
            guard += 1
            progressed = False
            for cat in categories:
                if len(picks) >= count:
                    break
                items = self.lessons_in_category(cat)
                idx = cursor[cat]
                while idx < len(items):
                    ex = items[idx]
                    idx += 1
                    if ex.id in completed or ex in picks:
                        continue
                    if not self.is_unlocked(ex, completed | {p.id for p in picks}):
                        continue
                    picks.append(ex)
                    progressed = True
                    break
                cursor[cat] = idx
            if not progressed:
                break
        return picks

    def search(self, query: str, difficulty: Optional[str] = None, limit: int = 50) -> list[Exercise]:
        """Case-insensitive substring match across title, objective, and
        concept_tags, optionally narrowed to one difficulty -- a flat
        lookup across the whole track's content, in level order, capped at
        `limit` so a broad/empty query doesn't dump the entire track."""
        needle = query.strip().lower()
        results: list[Exercise] = []
        for ex in self.all_in_order():
            if difficulty and ex.difficulty != difficulty:
                continue
            if needle:
                haystack = " ".join([ex.title, ex.objective, *ex.concept_tags]).lower()
                if needle not in haystack:
                    continue
            results.append(ex)
            if len(results) >= limit:
                break
        return results

    def recommend_practice(self, exercise_id: str, completed_ids: set[str], limit: int = 3) -> list[Exercise]:
        exercise = self.get(exercise_id)
        if exercise is None or not exercise.concept_tags:
            return []
        return self.recommend_practice_for_tags(set(exercise.concept_tags), completed_ids, limit, exclude={exercise_id})

    def recommend_practice_for_tags(
        self, tags: set[str], completed_ids: set[str], limit: int = 3, exclude: Optional[set[str]] = None,
    ) -> list[Exercise]:
        if not tags:
            return []
        exclude = exclude or set()
        candidates = [
            ex for ex in self.all_in_order()
            if ex.id not in completed_ids and ex.id not in exclude
            and set(ex.concept_tags) & tags
            and self.is_unlocked(ex, completed_ids)
        ]
        return candidates[:limit]
