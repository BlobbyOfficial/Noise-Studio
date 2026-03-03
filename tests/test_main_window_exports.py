from pathlib import Path

from ui.main_window import MainWindow


class DummyImagePanel:
    def __init__(self, has_image=True):
        self._has_image = has_image
        self.saved_to = None

    def get_current_image(self):
        return object() if self._has_image else None

    def save_to(self, path):
        self.saved_to = Path(path)


class DummySoundPanel:
    def __init__(self, has_audio=True):
        self._has_audio = has_audio
        self.saved_to = None

    def get_current_audio(self):
        return object() if self._has_audio else None

    def save_to(self, path):
        self.saved_to = Path(path)


def test_export_image_writes_file_to_images_dir(tmp_path, monkeypatch):
    app_dirs = {
        "base": tmp_path,
        "images": tmp_path / "images",
        "sounds": tmp_path / "sounds",
        "config": tmp_path / "config.json",
    }
    app_dirs["images"].mkdir()
    app_dirs["sounds"].mkdir()

    monkeypatch.setattr("ui.main_window.get_app_dirs", lambda: app_dirs)

    window = MainWindow()
    window.image_panel = DummyImagePanel(has_image=True)

    window.on_export_image_clicked()

    assert window.image_panel.saved_to is not None
    assert window.image_panel.saved_to.parent == app_dirs["images"]
    assert window.image_panel.saved_to.name.startswith("export_image_")


def test_export_sound_writes_file_to_sounds_dir(tmp_path, monkeypatch):
    app_dirs = {
        "base": tmp_path,
        "images": tmp_path / "images",
        "sounds": tmp_path / "sounds",
        "config": tmp_path / "config.json",
    }
    app_dirs["images"].mkdir()
    app_dirs["sounds"].mkdir()

    monkeypatch.setattr("ui.main_window.get_app_dirs", lambda: app_dirs)

    window = MainWindow()
    window.sound_panel = DummySoundPanel(has_audio=True)

    window.on_export_sound_clicked()

    assert window.sound_panel.saved_to is not None
    assert window.sound_panel.saved_to.parent == app_dirs["sounds"]
    assert window.sound_panel.saved_to.name.startswith("export_sound_")
