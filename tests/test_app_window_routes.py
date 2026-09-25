"""Route resolution for app_window.build_view_for_route -- the part of the
router that needs no live Flet session."""
from app.config.settings import Settings
from app.ui import app_window


def test_root_route_resolves_to_picker_or_setup(monkeypatch):
    seen = []
    monkeypatch.setitem(app_window._ROUTES, "/languages", lambda p, s: seen.append("languages") or "L")
    monkeypatch.setitem(app_window._ROUTES, "/setup", lambda p, s: seen.append("setup") or "S")

    class State:
        settings = Settings(setup_complete=True)

    assert app_window.build_view_for_route(None, State(), "/") == "L"
    assert app_window.build_view_for_route(None, State(), "") == "L"
    State.settings = Settings(setup_complete=False)
    assert app_window.build_view_for_route(None, State(), "/") == "S"
    assert seen == ["languages", "languages", "setup"]


def test_param_routes_pass_the_remainder(monkeypatch):
    monkeypatch.setitem(app_window._PARAM_ROUTES, "/lesson/", lambda p, s, arg: f"lesson:{arg}")
    assert app_window.build_view_for_route(None, object(), "/lesson/idioms_gotchas_01") == "lesson:idioms_gotchas_01"
