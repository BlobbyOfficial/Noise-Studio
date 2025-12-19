from ui.theme import apply_theme


def test_apply_theme_runs():
    # Should not raise and should return a boolean success indicator
    assert isinstance(apply_theme(), bool)
