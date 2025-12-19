"""
Image noise generation module.

Responsible for generating 2D noise patterns
such as white noise, Perlin noise, Simplex noise, etc.
"""

import numpy as np
from typing import Optional, Tuple

from .noise_common import create_numpy_rng, normalize_array


class ImageNoiseGenerator:
    """
    Main image noise generator class.
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None
    ):
        self.width = width
        self.height = height
        self.seed = seed
        self.rng = create_numpy_rng(seed)

    def generate_white_noise(self) -> np.ndarray:
        """
        Generate 2D white noise.

        Returns
        -------
        numpy.ndarray
            Array of shape (height, width) with values in [0, 1]
        """
        noise = self.rng.random((self.height, self.width))
        return noise

    def generate_perlin_noise(
        self,
        scale: float = 1.0,
        octaves: int = 1
    ) -> np.ndarray:
        """
        Placeholder for Perlin noise generation.
        """
        raise NotImplementedError("Perlin noise not implemented yet.")

    def resize(self, width: int, height: int):
        """
        Update canvas size.
        """
        self.width = width
        self.height = height

    def reset_seed(self, seed: Optional[int]):
        """
        Reset the RNG with a new seed.
        """
        self.seed = seed
        self.rng = create_numpy_rng(seed)
