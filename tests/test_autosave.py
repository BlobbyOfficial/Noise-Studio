import tempfile
from utils.config import get_app_dirs, ensure_app_dirs
from ui.panels.image_panel import ImagePanel
from ui.panels.sound_panel import SoundPanel
import os


def test_image_autosave(tmp_path):
    # redirect the app dirs to the temp path by monkeypatching get_app_dirs
    from utils import config
    orig = config.get_app_dirs

    def fake_get_app_dirs():
        return {"base": tmp_path, "images": tmp_path / "images", "sounds": tmp_path / "sound", "config": tmp_path / "config.json"}

    config.get_app_dirs = fake_get_app_dirs
    ensure_app_dirs()

    ip = ImagePanel()
    ip.on_generate_clicked()
    files = list((tmp_path / "images").glob("image_*.png"))
    assert len(files) >= 1

    # restore
    config.get_app_dirs = orig


def test_sound_autosave(tmp_path):
    from utils import config
    orig = config.get_app_dirs

    def fake_get_app_dirs():
        return {"base": tmp_path, "images": tmp_path / "images", "sounds": tmp_path / "sound", "config": tmp_path / "config.json"}

    config.get_app_dirs = fake_get_app_dirs
    ensure_app_dirs()

    sp = SoundPanel()
    sp.duration = 0.1
    sp.generate_noise()
    files = list((tmp_path / "sound").glob("sound_*.wav"))
    assert len(files) >= 1

    config.get_app_dirs = orig
