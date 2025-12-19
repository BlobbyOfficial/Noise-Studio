"""
Development helper utilities.

Used for:
- Debug printing
- Timing functions
- Temporary test runs
"""

import time
from contextlib import contextmanager


def debug_print(message: str):
    """
    Print a standardized debug message.
    """
    print(f"[DEBUG] {message}")


@contextmanager
def timer(label: str):
    """
    Context manager for timing code execution.

    Example:
        with timer("Noise generation"):
            generate_noise()
    """
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    print(f"[TIMER] {label}: {end - start:.4f}s")


def dev_banner():
    """
    Print a development banner.
    """
    print("=" * 40)
    print(" Noise Studio - Development Mode ")
    print("=" * 40)
