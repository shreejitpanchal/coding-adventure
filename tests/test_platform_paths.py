from app.config import platform_paths


def test_uses_flet_app_storage_data_env_var_when_set(tmp_path, monkeypatch):
    android_dir = tmp_path / "android_data"
    monkeypatch.setenv("FLET_APP_STORAGE_DATA", str(android_dir))

    data_dir = platform_paths.resolve_platform_data_dir()

    assert data_dir == android_dir
    assert data_dir.is_dir()


def test_falls_back_to_repo_root_data_when_env_var_unset(monkeypatch):
    monkeypatch.delenv("FLET_APP_STORAGE_DATA", raising=False)

    data_dir = platform_paths.resolve_platform_data_dir()

    assert data_dir.name == "data"
    assert data_dir.parent == platform_paths.Path(__file__).resolve().parent.parent
    assert data_dir.is_dir()
