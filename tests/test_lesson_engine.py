"""ExerciseEngine behaviour. Track-wide content invariants (counts,
contiguous levels, valid regexes, ...) live in test_content_lint.py so
adding content never means editing a test here."""
import pytest

from app.engine.content_loader import ContentError
from app.engine.lesson_engine import ExerciseEngine
from app.engine import lesson_engine as lesson_engine_module

_MINIMAL_EXERCISE_TEMPLATE = (
    "id: {id}\nlanguage: python\nlevel: {level}\ntitle: {title}\n"
    "objective: obj\nexplanation: exp\nexpected_output: x\n"
    "category: {category}\ncategory_level: {category_level}\n"
)


def _write_exercise(directory, filename, exercise_id, level=1, title="Title", category="general", category_level=1):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / filename).write_text(
        _MINIMAL_EXERCISE_TEMPLATE.format(
            id=exercise_id, level=level, title=title, category=category, category_level=category_level,
        ),
        encoding="utf-8",
    )


@pytest.fixture
def small_engine(tmp_path):
    d = tmp_path / "lessons"
    _write_exercise(d, "a1.yaml", "a_01", level=1, category="alpha", category_level=1)
    _write_exercise(d, "a2.yaml", "a_02", level=2, category="alpha", category_level=2)
    _write_exercise(d, "a3.yaml", "a_03", level=3, category="alpha", category_level=3)
    _write_exercise(d, "b1.yaml", "b_01", level=4, category="beta", category_level=1)
    _write_exercise(d, "b2.yaml", "b_02", level=5, category="beta", category_level=2)
    return ExerciseEngine("python", content_dir=d, custom_content_dir=tmp_path / "none")


# -- real content smoke checks --------------------------------------------

def test_loads_python_content():
    engine = ExerciseEngine("python")
    assert len(engine) > 0
    assert engine.has("idioms_gotchas_01")
    assert not engine.has("does_not_exist")
    assert "gotcha_gauntlet" in engine.categories()


def test_categories_follow_level_order():
    engine = ExerciseEngine("node")
    assert engine.categories()[-1] == "gotcha_gauntlet"


def test_ai_and_architecture_always_fully_unlocked():
    for language in ("ai", "architecture"):
        engine = ExerciseEngine(language)
        assert len(engine) > 0
        assert all(engine.is_unlocked(ex, completed_ids=set()) for ex in engine.all_in_order())


def test_architecture_is_entirely_conceptual():
    engine = ExerciseEngine("architecture")
    assert all(not ex.requires_code for ex in engine.all_in_order())


def test_ai_only_agent_365_is_conceptual():
    engine = ExerciseEngine("ai")
    for ex in engine.all_in_order():
        assert ex.requires_code is (ex.category != "microsoft_agent_365"), ex.id


# -- unlock logic ---------------------------------------------------------

def test_category_level_1_always_unlocked(small_engine):
    assert small_engine.is_unlocked(small_engine.get("a_01"), completed_ids=set())
    assert small_engine.is_unlocked(small_engine.get("b_01"), completed_ids=set())


def test_locked_until_every_earlier_level_complete(small_engine):
    third = small_engine.get("a_03")
    assert not small_engine.is_unlocked(third, completed_ids=set())
    assert not small_engine.is_unlocked(third, completed_ids={"a_02"})  # a_01 still missing
    assert small_engine.is_unlocked(third, completed_ids={"a_01", "a_02"})


def test_other_categories_do_not_affect_unlock(small_engine):
    assert small_engine.is_unlocked(small_engine.get("b_02"), completed_ids={"b_01"})
    assert not small_engine.is_unlocked(small_engine.get("b_02"), completed_ids={"a_01", "a_02", "a_03"})


def test_java_locked_normally_when_not_android(monkeypatch):
    monkeypatch.setattr(lesson_engine_module, "is_android", lambda: False)
    engine = ExerciseEngine("java")
    lessons = engine.lessons_in_category(engine.categories()[0])
    assert len(lessons) > 1
    assert not engine.is_unlocked(lessons[1], completed_ids=set())


def test_java_all_unlocked_on_android(monkeypatch):
    monkeypatch.setattr(lesson_engine_module, "is_android", lambda: True)
    engine = ExerciseEngine("java")
    assert all(engine.is_unlocked(ex, completed_ids=set()) for ex in engine.all_in_order())


def test_python_still_gated_on_android(monkeypatch):
    monkeypatch.setattr(lesson_engine_module, "is_android", lambda: True)
    engine = ExerciseEngine("python")
    second = engine.get("idioms_gotchas_02")
    assert not engine.is_unlocked(second, completed_ids=set())


def test_next_unlocked_in_category(small_engine):
    assert small_engine.next_unlocked_in_category("alpha", set()).id == "a_01"
    assert small_engine.next_unlocked_in_category("alpha", {"a_01"}).id == "a_02"
    assert small_engine.next_unlocked_in_category("alpha", {"a_01", "a_02", "a_03"}) is None


def test_category_completion_for(small_engine):
    assert small_engine.category_completion_for({"a_01", "b_01", "b_02"}) == {"alpha": (1, 3), "beta": (2, 2)}


# -- daily refresher / search / recommendations ---------------------------

def test_daily_refresher_round_robins_categories(small_engine):
    picks = small_engine.daily_refresher(completed_ids=set(), count=4)
    assert [ex.id for ex in picks] == ["a_01", "b_01", "a_02", "b_02"]


def test_daily_refresher_respects_completion_and_unlocks(small_engine):
    picks = small_engine.daily_refresher(completed_ids={"a_01", "b_01", "b_02"}, count=5)
    assert [ex.id for ex in picks] == ["a_02", "a_03"]


def test_daily_refresher_zero_count(small_engine):
    assert small_engine.daily_refresher(set(), count=0) == []


def test_daily_refresher_spans_categories_on_real_content():
    engine = ExerciseEngine("python")
    picks = engine.daily_refresher(completed_ids=set(), count=5)
    assert len(picks) == 5
    assert len({ex.category for ex in picks}) == 5


def test_recommend_practice_excludes_self_and_completed():
    engine = ExerciseEngine("python")
    suggestions = engine.recommend_practice("gotcha_gauntlet_03", completed_ids=set())
    assert "gotcha_gauntlet_03" not in [ex.id for ex in suggestions]


def test_search_matches_title_objective_and_concept_tags():
    engine = ExerciseEngine("python")
    by_title = engine.search("mutable default")
    assert any(ex.id == "idioms_gotchas_01" for ex in by_title)

    by_tag = engine.search("closures")
    assert by_tag
    assert all("closures" in " ".join([ex.title, ex.objective, *ex.concept_tags]).lower() for ex in by_tag)


def test_search_filters_by_difficulty_and_limit():
    engine = ExerciseEngine("python")
    results = engine.search("", difficulty="gotcha")
    assert results and all(ex.difficulty == "gotcha" for ex in results)
    assert len(engine.search("", limit=3)) == 3


# -- loading --------------------------------------------------------------

def test_missing_content_dir_yields_empty_engine(tmp_path):
    engine = ExerciseEngine("nonexistent", content_dir=tmp_path / "missing", custom_content_dir=tmp_path / "none")
    assert len(engine) == 0
    assert engine.categories() == []


def test_custom_content_overlay_loads_after_builtin(tmp_path):
    builtin_dir = tmp_path / "builtin"
    custom_dir = tmp_path / "custom"
    _write_exercise(builtin_dir, "a.yaml", "builtin_a", level=1)
    _write_exercise(custom_dir, "b.yaml", "custom_b", level=2, category_level=2)

    engine = ExerciseEngine("python", content_dir=builtin_dir, custom_content_dir=custom_dir)
    assert engine.has("builtin_a")
    assert engine.has("custom_b")
    assert len(engine) == 2


def test_custom_content_duplicate_id_fails_loud(tmp_path):
    builtin_dir = tmp_path / "builtin"
    custom_dir = tmp_path / "custom"
    _write_exercise(builtin_dir, "a.yaml", "dup_id", level=1)
    _write_exercise(custom_dir, "b.yaml", "dup_id", level=2)

    with pytest.raises(ContentError, match="dup_id") as excinfo:
        ExerciseEngine("python", content_dir=builtin_dir, custom_content_dir=custom_dir)
    assert "b.yaml" in str(excinfo.value)


def test_malformed_exercise_error_names_the_file(tmp_path):
    d = tmp_path / "lessons"
    d.mkdir()
    (d / "bad.yaml").write_text("id: bad\nlanguage: python\nlevel: 1\ntitle: t\nobjective: o\nexplanation: e\nhnits: []\n", encoding="utf-8")
    with pytest.raises(ContentError, match="hnits") as excinfo:
        ExerciseEngine("python", content_dir=d, custom_content_dir=tmp_path / "none")
    assert "bad.yaml" in str(excinfo.value)


def test_invalid_yaml_error_names_the_file(tmp_path):
    d = tmp_path / "lessons"
    d.mkdir()
    (d / "broken.yaml").write_text("id: [unclosed\n", encoding="utf-8")
    with pytest.raises(ContentError, match="broken.yaml"):
        ExerciseEngine("python", content_dir=d, custom_content_dir=tmp_path / "none")
