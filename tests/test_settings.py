import json

from app.config.settings import Settings, load_settings, save_settings


def test_missing_file_gives_defaults(tmp_path):
    settings = load_settings(tmp_path / "settings.json")
    assert settings == Settings()


def test_round_trip(tmp_path):
    path = tmp_path / "settings.json"
    save_settings(Settings(handle="Ada", theme="dracula", daily_refresher_size=8, weekly_goal=25), path)
    loaded = load_settings(path)
    assert loaded.handle == "Ada"
    assert loaded.theme == "dracula"
    assert loaded.daily_refresher_size == 8
    assert loaded.weekly_goal == 25


def test_defaults_for_new_installs():
    s = Settings()
    assert s.theme == "aurora"
    assert s.weekly_goal == 10


def test_unknown_keys_are_ignored(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text(json.dumps({"handle": "Ada", "from_the_future": 1}), encoding="utf-8")
    assert load_settings(path).handle == "Ada"


def test_corrupt_file_is_quarantined_not_deleted(tmp_path, caplog):
    path = tmp_path / "settings.json"
    path.write_text("{not json", encoding="utf-8")
    with caplog.at_level("WARNING"):
        settings = load_settings(path)
    assert settings == Settings()
    assert not path.exists()
    quarantined = list(tmp_path.glob("settings.json.corrupt-*"))
    assert len(quarantined) == 1
    assert quarantined[0].read_text(encoding="utf-8") == "{not json"
    assert "unreadable" in caplog.text


def test_non_object_json_is_treated_as_corrupt(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text("[1, 2, 3]", encoding="utf-8")
    assert load_settings(path) == Settings()
    assert list(tmp_path.glob("settings.json.corrupt-*"))
