import pytest

from app.engine.content_loader import ContentError, build_model
from app.engine.exercise import Exercise
from app.engine.quiz import QuizQuestion

_BASE = dict(id="ex", title="t", language="python", level=1, objective="o", explanation="e")


def _check(**overrides):
    q = {"question": "?", "options": ["a", "b", "c", "d"], "correct": 1, "explanation": "because"}
    q.update(overrides)
    return q


def test_comprehension_check_parsed_into_quiz_questions_with_derived_ids():
    ex = Exercise(**_BASE, requires_code=False, comprehension_check=[_check(), _check(correct=3)])
    assert all(isinstance(q, QuizQuestion) for q in ex.comprehension_check)
    assert [q.id for q in ex.comprehension_check] == ["ex_check_1", "ex_check_2"]
    assert ex.comprehension_check[1].correct == 3


def test_already_parsed_questions_pass_through():
    q = QuizQuestion(id="q", question="?", options=["a", "b"], correct=0)
    ex = Exercise(**_BASE, requires_code=False, comprehension_check=[q])
    assert ex.comprehension_check[0] is q


def test_correct_index_out_of_range_fails_at_load():
    with pytest.raises(ValueError, match="ex_check_1"):
        Exercise(**_BASE, requires_code=False, comprehension_check=[_check(correct=4)])


def test_too_few_options_fails_at_load():
    with pytest.raises(ValueError, match="at least 2"):
        Exercise(**_BASE, requires_code=False, comprehension_check=[_check(options=["only"], correct=0)])


def test_unknown_question_key_names_the_question():
    with pytest.raises(ValueError, match="ex_check_1"):
        Exercise(**_BASE, requires_code=False, comprehension_check=[_check(explanaton="typo")])


def test_conceptual_exercise_without_questions_is_rejected():
    with pytest.raises(ValueError, match="comprehension_check is empty"):
        Exercise(**_BASE, requires_code=False)


def test_bad_difficulty_rejected():
    with pytest.raises(ValueError, match="difficulty"):
        Exercise(**_BASE, difficulty="impossible")


def test_build_model_error_carries_the_file_path(tmp_path):
    path = tmp_path / "broken.yaml"
    with pytest.raises(ContentError) as excinfo:
        build_model(Exercise, {**_BASE, "hnits": []}, path)
    message = str(excinfo.value)
    assert str(path) in message
    assert "hnits" in message


def test_build_model_rejects_non_mapping(tmp_path):
    with pytest.raises(ContentError, match="mapping"):
        build_model(Exercise, ["not", "a", "dict"], tmp_path / "x.yaml")
