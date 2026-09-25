"""Content lint: one parametrized pass over every track's YAML.

Replaces hard-coded "this track has exactly N exercises" assertions,
which broke on every content addition, with the invariants that
actually matter for the app to work:

- every file loads into the Exercise model (which itself validates
  difficulty, comprehension checks, and category_level >= 1);
- ids and global `level` values are unique within a track;
- each category's `category_level`s run 1..N with no gaps, since
  is_unlocked() gates on "every earlier level complete";
- a code exercise has something to validate against (expected_output or
  expected_output_pattern), and its contains_patterns compile as regex;
- every category has display metadata so the topic browser never falls
  back to the generic label by accident;
- the track's quiz bank loads with unique ids.
"""
from __future__ import annotations

import re

import pytest

from app.engine.categories import CATEGORY_META
from app.engine.languages import LANGUAGE_ORDER
from app.engine.lesson_engine import ExerciseEngine
from app.engine.quiz_engine import QuizEngine

TRACKS = LANGUAGE_ORDER


@pytest.fixture(scope="module", params=TRACKS)
def track(request):
    return request.param


@pytest.fixture(scope="module")
def engine(track):
    return ExerciseEngine(track)


def test_track_has_content(engine, track):
    assert len(engine) > 0, f"{track} has no exercises"


def test_global_levels_unique(engine, track):
    levels = [ex.level for ex in engine.all_in_order()]
    duplicates = sorted({lvl for lvl in levels if levels.count(lvl) > 1})
    assert not duplicates, f"{track}: duplicate level values {duplicates} -- ordering would be unstable"


def test_category_levels_contiguous(engine, track):
    for category in engine.categories():
        levels = [ex.category_level for ex in engine.lessons_in_category(category)]
        assert levels == list(range(1, len(levels) + 1)), (
            f"{track}/{category}: category_level must run 1..{len(levels)} without gaps, got {levels}"
        )


def test_every_category_has_display_meta(engine, track):
    missing = [c for c in engine.categories() if c not in CATEGORY_META]
    assert not missing, f"{track}: add CATEGORY_META entries for {missing}"


def test_code_exercises_have_something_to_validate(engine, track):
    offenders = [
        ex.id for ex in engine.all_in_order()
        if ex.requires_code and not (ex.expected_output or ex.expected_output_pattern)
    ]
    assert not offenders, f"{track}: no expected_output/expected_output_pattern on {offenders}"


def test_contains_patterns_are_valid_regex(engine, track):
    for ex in engine.all_in_order():
        for pattern in ex.contains_patterns or []:
            try:
                re.compile(pattern)
            except re.error as exc:
                pytest.fail(f"{track}/{ex.id}: contains_patterns entry {pattern!r} is not a valid regex ({exc})")


def test_expected_output_patterns_are_valid_regex(engine, track):
    for ex in engine.all_in_order():
        if ex.expected_output_pattern:
            re.compile(ex.expected_output_pattern)


def test_conceptual_exercises_have_checks(engine, track):
    for ex in engine.all_in_order():
        if not ex.requires_code:
            assert len(ex.comprehension_check) >= 2, f"{track}/{ex.id}: needs at least two check questions"
            for q in ex.comprehension_check:
                assert len(q.options) == 4, f"{track}/{ex.id}: {q.id} should offer four options"


def test_quiz_bank_loads(track):
    quiz = QuizEngine(track)
    assert len(quiz) > 0, f"{track}: quiz bank is empty or missing"
    ids = [q.id for q in quiz.all_questions()]
    assert len(ids) == len(set(ids))
