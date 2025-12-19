from ui.panels.image_panel import ImagePanel
from ui.panels.sound_panel import SoundPanel


def test_image_panel_resolution_change_no_live_preview():
    p = ImagePanel()
    p.live_preview = False
    p.on_resolution_changed(128, 96)
    assert p.width == 128 and p.height == 96
    assert p.current_image is None


def test_sound_panel_generate_noise_normalized():
    s = SoundPanel()
    s.duration = 0.2
    s.sample_rate = 16000
    audio = s.generate_noise()
    assert audio is not None
    assert len(audio) == int(16000 * 0.2)
    assert abs(audio).max() <= 1.0
