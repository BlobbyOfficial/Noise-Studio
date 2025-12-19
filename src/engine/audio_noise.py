"""
Audio noise generation module.

Responsible for generating procedural audio noise
such as white, pink, brown, and advanced noise types.
"""

import numpy as np
from typing import Optional

from .noise_common import create_numpy_rng


class AudioNoiseGenerator:
    """
    Main audio noise generator class.
    """

    def __init__(
        self,
        sample_rate: int = 44100,
        seed: Optional[int] = None
    ):
        self.sample_rate = sample_rate
        self.seed = seed
        self.rng = create_numpy_rng(seed)

    def generate_white_noise(
        self,
        duration_seconds: float,
        amplitude: float = 1.0
    ) -> np.ndarray:
        """
        Generate white noise.

        Returns
        -------
        numpy.ndarray
            Audio samples in range [-1, 1]
        """
        num_samples = int(self.sample_rate * duration_seconds)
        noise = self.rng.uniform(-1.0, 1.0, num_samples)
        return noise * amplitude

    def generate_pink_noise(self, duration_seconds: float) -> np.ndarray:
        """
        Placeholder for pink noise generation.
        """
        raise NotImplementedError("Pink noise not implemented yet.")

    def generate_brown_noise(self, duration_seconds: float) -> np.ndarray:
        """
        Placeholder for brown (Brownian) noise generation.
        """
        raise NotImplementedError("Brown noise not implemented yet.")

    def reset_seed(self, seed: Optional[int]):
        """
        Reset the RNG with a new seed.
        """
        self.seed = seed
        self.rng = create_numpy_rng(seed)
