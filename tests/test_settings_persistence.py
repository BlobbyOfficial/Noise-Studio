from utils.config import get_app_dirs, ensure_app_dirs, save_settings, load_settings
import tempfile


def test_settings_persistence(tmp_path):
    # monkeypatch get_app_dirs to use tmp_path
    from utils import config
    orig = config.get_app_dirs

    def fake_get_app_dirs():
        return {"base": tmp_path, "images": tmp_path / "images", "sounds": tmp_path / "sound", "config": tmp_path / "config.json"}

    config.get_app_dirs = fake_get_app_dirs
    ensure_app_dirs()
    settings = {"theme": "light", "sample_rate": 22050, "live_preview": False}
    save_settings(settings)
    loaded = load_settings()
    assert loaded["sample_rate"] == 22050
    assert loaded["theme"] == "light"

    config.get_app_dirs = orig
