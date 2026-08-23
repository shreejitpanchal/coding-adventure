from app.engine.lesson_engine import ExerciseEngine


def test_loads_python_content():
    engine = ExerciseEngine("python")
    assert len(engine) == 75
    assert engine.has("idioms_gotchas_01")
    assert not engine.has("does_not_exist")


def test_categories_derived_from_content():
    engine = ExerciseEngine("python")
    categories = engine.categories()
    assert "idioms_gotchas" in categories
    assert "gotcha_gauntlet" in categories
    assert "thread_scheduling" in categories
    assert "observability" in categories
    assert len(categories) == 14


def test_category_level_1_always_unlocked():
    engine = ExerciseEngine("python")
    first = engine.get("idioms_gotchas_01")
    assert engine.is_unlocked(first, completed_ids=set())


def test_locked_until_earlier_levels_complete():
    engine = ExerciseEngine("python")
    second = engine.get("idioms_gotchas_02")
    assert not engine.is_unlocked(second, completed_ids=set())
    assert engine.is_unlocked(second, completed_ids={"idioms_gotchas_01"})


def test_next_unlocked_in_category():
    engine = ExerciseEngine("python")
    nxt = engine.next_unlocked_in_category("idioms_gotchas", completed_ids=set())
    assert nxt.id == "idioms_gotchas_01"
    nxt = engine.next_unlocked_in_category("idioms_gotchas", completed_ids={"idioms_gotchas_01"})
    assert nxt.id == "idioms_gotchas_02"


def test_daily_refresher_spans_categories():
    engine = ExerciseEngine("python")
    picks = engine.daily_refresher(completed_ids=set(), count=5)
    assert len(picks) == 5
    categories = {ex.category for ex in picks}
    assert len(categories) == 5


def test_recommend_practice_excludes_self_and_completed():
    engine = ExerciseEngine("python")
    suggestions = engine.recommend_practice("gotcha_gauntlet_03", completed_ids=set())
    ids = [ex.id for ex in suggestions]
    assert "gotcha_gauntlet_03" not in ids


def test_missing_content_dir_yields_empty_engine(tmp_path):
    engine = ExerciseEngine("nonexistent", content_dir=tmp_path / "missing")
    assert len(engine) == 0
    assert engine.categories() == []
