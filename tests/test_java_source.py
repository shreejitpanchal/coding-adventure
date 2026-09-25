from app.execution.java_source import detect_class_name


def test_public_class_wins_over_earlier_non_public_class():
    code = "class Helper {}\npublic final class Main { }"
    assert detect_class_name(code) == "Main"


def test_first_class_when_nothing_is_public():
    assert detect_class_name("class A {}\nclass B {}") == "A"


def test_default_when_no_class_at_all():
    assert detect_class_name("// nothing here") == "Solution"
    assert detect_class_name("", default="SolutionTest") == "SolutionTest"


def test_abstract_public_class():
    assert detect_class_name("public abstract class Shape {}") == "Shape"
