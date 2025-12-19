from engine.image_noise import ImageNoiseGenerator


def test_white_noise_shape_and_range():
    gen = ImageNoiseGenerator(64, 32, seed=42)
    arr = gen.generate_white_noise()
    assert arr.shape == (32, 64)
    assert arr.min() >= 0.0 and arr.max() <= 1.0
