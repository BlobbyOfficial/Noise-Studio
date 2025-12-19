"""
Common utilities for noise generation.

Shared logic such as:
- Seed handling
- Random number generation
- Validation helpers
"""

import random
import numpy as np
from typing import Optional


def create_rng(seed: Optional[int] = None):
    """
    Create and return a deterministic random number generator.

    Parameters
    ----------
    seed : int or None
        If None, a random seed is used.

    Returns
    -------
    random.Random
    """
    return random.Random(seed)


def create_numpy_rng(seed: Optional[int] = None):
    """
    Create and return a NumPy random generator.

    Parameters
    ----------
    seed : int or None

    Returns
    -------
    numpy.random.Generator
    """
    return np.random.default_rng(seed)


def clamp(value: float, minimum: float, maximum: float) -> float:
    """
    Clamp a value between a minimum and maximum.
    """
    return max(minimum, min(value, maximum))


def normalize_array(arr: np.ndarray) -> np.ndarray:
    """
    Normalize a NumPy array to the range [0, 1].
    """
    min_val = arr.min()
    max_val = arr.max()

    if max_val == min_val:
        return np.zeros_like(arr)

    return (arr - min_val) / (max_val - min_val)
