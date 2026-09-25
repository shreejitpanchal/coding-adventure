import pytest

from app.engine.content_loader import ContentError
from app.engine.quiz import QuizQuestion
from app.engine.quiz_engine import QuizEngine, shuffle_options


def test_loads_python_quiz_bank():
    quiz = QuizEngine("python")
    assert len(quiz) > 0


def test_session_size_and_option_shuffle_preserve_answer():
    quiz = QuizEngine("python")
    session = quiz.start_session(5)
    assert len(session) == 5
    originals = {q.id: q for q in quiz.all_questions()}
    for q in session:
        original = originals[q.id]
        assert sorted(q.options) == sorted(original.options)
        assert q.options[q.correct] == original.options[original.correct]


def test_shuffle_options_never_changes_the_correct_text():
    q = QuizQuestion(id="x", question="?", options=["a", "b", "c", "d"], correct=2)
    for _ in range(20):
        shuffled = shuffle_options(q)
        assert shuffled.options[shuffled.correct] == "c"


def test_session_for_tags_falls_back_to_full_pool_when_no_match():
    quiz = QuizEngine("python")
    session = quiz.start_session_for_tags({"no_such_tag"}, count=3)
    assert len(session) == 3


def test_missing_quiz_file_yields_empty_engine(tmp_path):
    quiz = QuizEngine("nowhere", quiz_path=tmp_path / "missing.yaml")
    assert len(quiz) == 0
    assert quiz.start_session(5) == []


def test_malformed_question_fails_with_file_path(tmp_path):
    path = tmp_path / "quiz.yaml"
    path.write_text(
        "questions:\n  - id: q1\n    question: '?'\n    options: ['only one']\n    correct: 0\n",
        encoding="utf-8",
    )
    with pytest.raises(ContentError, match="q1") as excinfo:
        QuizEngine("x", quiz_path=path)
    assert str(path) in str(excinfo.value)


def test_duplicate_question_id_fails_loud(tmp_path):
    path = tmp_path / "quiz.yaml"
    body = "    question: '?'\n    options: ['a', 'b']\n    correct: 0\n"
    path.write_text(f"questions:\n  - id: dup\n{body}  - id: dup\n{body}", encoding="utf-8")
    with pytest.raises(ContentError, match="duplicate"):
        QuizEngine("x", quiz_path=path)
