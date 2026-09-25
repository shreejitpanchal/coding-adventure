from app.engine.error_insights import summarize_errors
from app.engine.lesson_engine import ExerciseEngine

NAME_ERR = 'File "<exercise>", line 2\nNameError: name x is not defined\n'
ZERO_ERR = "ZeroDivisionError: division by zero\n"


def test_groups_by_friendly_message_and_counts_most_common_first():
    engine = ExerciseEngine("python")
    a, b = engine.all_in_order()[0].id, engine.all_in_order()[1].id
    rows = [(a, NAME_ERR), (b, NAME_ERR), (a, ZERO_ERR), (None, NAME_ERR)]
    insights = summarize_errors(rows, engine, "python")
    assert [i.message for i in insights] == ["Undefined name.", "Division by zero."]
    top = insights[0]
    assert top.count == 3
    assert top.lesson_ids == [a, b]  # distinct, in order seen (most recent first)
    assert top.hint
    expected_tags = set(engine.get(a).concept_tags) | set(engine.get(b).concept_tags)
    assert set(top.concept_tags) <= expected_tags


def test_limit_and_unknown_language_bucket():
    engine = ExerciseEngine("python")
    rows = [("x", f"Error{i}: boom") for i in range(10)]
    insights = summarize_errors(rows, engine, "python", limit=1)
    assert len(insights) == 1
    assert insights[0].count == 10  # all unknown -> one generic bucket
    assert insights[0].lesson_ids == ["x"]


def test_empty_rows_yield_no_insights():
    assert summarize_errors([], ExerciseEngine("python"), "python") == []
