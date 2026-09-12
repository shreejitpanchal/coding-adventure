from app.engine.lesson_engine import ExerciseEngine
from app.engine import lesson_engine as lesson_engine_module


def test_loads_python_content():
    engine = ExerciseEngine("python")
    assert len(engine) == 455
    assert engine.has("idioms_gotchas_01")
    assert engine.has("idioms_gotchas_50")
    assert engine.has("core_refresher_50")
    assert engine.has("data_structures_50")
    assert engine.has("stdlib_deep_dive_50")
    assert engine.has("gotcha_gauntlet_50")
    assert engine.has("concurrency_async_50")
    assert engine.has("functional_programming_50")
    assert engine.has("packaging_15")
    assert engine.has("deployment_15")
    assert engine.has("observability_15")
    assert engine.has("dependency_management_15")
    assert engine.has("thread_scheduling_15")
    assert engine.has("sync_vs_async_15")
    assert engine.has("recursion_15")
    assert not engine.has("does_not_exist")
    # All 14 Python-track categories have now been expanded: the seven
    # broad categories (idioms_gotchas, core_refresher, data_structures,
    # stdlib_deep_dive, gotcha_gauntlet, concurrency_async,
    # functional_programming) to 50 exercises each, and the seven narrow
    # categories (packaging, deployment, observability,
    # dependency_management, thread_scheduling, sync_vs_async, recursion)
    # to 15 exercises each -- 350 + 105 = 455 total.
    assert len(engine.lessons_in_category("idioms_gotchas")) == 50
    assert len(engine.lessons_in_category("core_refresher")) == 50
    assert len(engine.lessons_in_category("data_structures")) == 50
    assert len(engine.lessons_in_category("stdlib_deep_dive")) == 50
    assert len(engine.lessons_in_category("gotcha_gauntlet")) == 50
    assert len(engine.lessons_in_category("concurrency_async")) == 50
    assert len(engine.lessons_in_category("functional_programming")) == 50
    assert len(engine.lessons_in_category("packaging")) == 15
    assert len(engine.lessons_in_category("deployment")) == 15
    assert len(engine.lessons_in_category("observability")) == 15
    assert len(engine.lessons_in_category("dependency_management")) == 15
    assert len(engine.lessons_in_category("thread_scheduling")) == 15
    assert len(engine.lessons_in_category("sync_vs_async")) == 15
    assert len(engine.lessons_in_category("recursion")) == 15


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


def test_loads_node_content():
    engine = ExerciseEngine("node")
    assert len(engine) == 60
    assert engine.has("idioms_gotchas_01")
    categories = engine.categories()
    assert set(categories) == {
        "idioms_gotchas", "core_refresher", "data_structures",
        "stdlib_deep_dive", "concurrency_async", "dependency_management",
        "sync_vs_async", "functional_programming", "recursion",
        "observability", "deployment", "gotcha_gauntlet",
    }
    assert categories[-1] == "gotcha_gauntlet"


def test_java_locked_normally_when_not_android(monkeypatch):
    monkeypatch.setattr(lesson_engine_module, "is_android", lambda: False)
    engine = ExerciseEngine("java")
    lessons = engine.lessons_in_category(engine.categories()[0])
    if len(lessons) > 1:
        assert not engine.is_unlocked(lessons[1], completed_ids=set())


def test_java_all_unlocked_on_android(monkeypatch):
    monkeypatch.setattr(lesson_engine_module, "is_android", lambda: True)
    engine = ExerciseEngine("java")
    for ex in engine.all_in_order():
        assert engine.is_unlocked(ex, completed_ids=set())


def test_python_still_gated_on_android(monkeypatch):
    monkeypatch.setattr(lesson_engine_module, "is_android", lambda: True)
    engine = ExerciseEngine("python")
    second = engine.get("idioms_gotchas_02")
    assert not engine.is_unlocked(second, completed_ids=set())


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


def test_loads_java_content():
    engine = ExerciseEngine("java")
    assert len(engine) == 70
    assert engine.has("gotcha_gauntlet_05")
    categories = engine.categories()
    assert len(categories) == 14
    assert "gotcha_gauntlet" in categories
    assert "observability" in categories


def test_loads_cpp_content():
    engine = ExerciseEngine("cpp")
    assert len(engine) == 50
    assert engine.has("gotcha_gauntlet_05")
    categories = engine.categories()
    assert len(categories) == 10
    assert "gotcha_gauntlet" in categories
    assert "concurrency_async" in categories
    assert "thread_scheduling" in categories
    assert "sync_vs_async" in categories
    assert "functional_programming" in categories
    assert "recursion" in categories
    assert categories[-1] == "gotcha_gauntlet"


def test_loads_spring_content():
    engine = ExerciseEngine("spring")
    assert len(engine) == 30
    assert engine.has("dependency_injection_05")
    categories = engine.categories()
    assert len(categories) == 6
    assert "dependency_injection" in categories
    assert "bean_lifecycle" in categories
    assert "configuration_profiles" in categories
    assert "events" in categories
    assert "aop" in categories
    assert "resilience" in categories


def test_loads_ai_content():
    engine = ExerciseEngine("ai")
    assert len(engine) == 405
    assert engine.has("ai_01")
    assert engine.has("ai_405")
    categories = engine.categories()
    assert len(categories) == 9
    assert categories == [
        "ml_fundamentals",
        "rag",
        "agentic_frameworks",
        "mcp",
        "microsoft_agent_365",
        "langchain",
        "langgraph",
        "langsmith",
        "solace_agent_mesh",
    ]
    # Every AI-track category has been expanded from 5 to 50 exercises,
    # except microsoft_agent_365 (deliberately staying at 5, since it's
    # conceptual comprehension-check content with no hand-codeable
    # mechanic to expand).
    expected_sizes = {
        "ml_fundamentals": 50,
        "rag": 50,
        "agentic_frameworks": 50,
        "mcp": 50,
        "microsoft_agent_365": 5,
        "langchain": 50,
        "langgraph": 50,
        "langsmith": 50,
        "solace_agent_mesh": 50,
    }
    for category, expected_count in expected_sizes.items():
        assert len(engine.lessons_in_category(category)) == expected_count, category

    no_code_categories = {"microsoft_agent_365"}
    for ex in engine.all_in_order():
        if ex.category in no_code_categories:
            assert ex.requires_code is False
            assert len(ex.comprehension_check) >= 2
        else:
            assert ex.requires_code is True


def test_ai_and_architecture_always_fully_unlocked():
    for language in ("ai", "architecture"):
        engine = ExerciseEngine(language)
        assert len(engine) > 0
        assert all(engine.is_unlocked(ex, completed_ids=set()) for ex in engine.all_in_order())


def test_loads_architecture_content():
    engine = ExerciseEngine("architecture")
    assert len(engine) == 50
    assert engine.has("event_driven_architecture_01")
    categories = engine.categories()
    assert categories == [
        "event_driven_architecture",
        "microservices",
        "cqrs",
        "saga_pattern",
        "strangler_fig",
        "domain_driven_design",
        "hexagonal_architecture",
        "api_gateway",
        "circuit_breaker",
        "idempotency",
    ]
    for category in categories:
        assert len(engine.lessons_in_category(category)) == 5
    for ex in engine.all_in_order():
        assert ex.requires_code is False
        assert len(ex.comprehension_check) >= 2
