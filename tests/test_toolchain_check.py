from app.execution import toolchain_check
from app.execution.toolchain_check import check_toolchain, get_install_guide


def test_python_ai_architecture_need_nothing():
    for language in ("python", "ai", "architecture"):
        status = check_toolchain(language)
        assert status.available
        assert status.missing == []


def test_reports_exactly_the_missing_tools(monkeypatch):
    present = {"java"}
    monkeypatch.setattr(toolchain_check.shutil, "which", lambda tool: "/bin/x" if tool in present else None)
    status = check_toolchain("java")
    assert not status.available
    assert status.missing == ["javac"]
    assert "adoptium" in status.install_hint


def test_unknown_language_is_treated_as_available():
    status = check_toolchain("brainfuck")
    assert status.available
    assert status.install_hint == ""


def test_install_guide_falls_back_to_first_os_when_unknown(monkeypatch):
    monkeypatch.setattr(toolchain_check.platform, "system", lambda: "Plan9")
    steps, verify = get_install_guide("node")
    assert steps  # some OS's steps rather than nothing
    assert verify == "node --version"


def test_install_guide_none_for_tracks_without_toolchain():
    assert get_install_guide("python") is None
    assert get_install_guide("architecture") is None
