from engine.audio_noise import AudioNoiseGenerator


def test_white_noise_length_and_range():
    gen = AudioNoiseGenerator(sample_rate=48000, seed=1)
    arr = gen.generate_white_noise(0.5)
    assert len(arr) == int(48000 * 0.5)
    assert arr.min() >= -1.0 and arr.max() <= 1.0
