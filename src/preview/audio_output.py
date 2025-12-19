"""
Audio preview output module.

Handles playback of preview-quality audio noise.
"""

from typing import Optional

import numpy as np


class AudioPreviewPlayer:
    """
    Handles audio playback for previews.
    """

    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self._is_playing = False

    def play(self, audio_data: np.ndarray):
        """
        Play audio data.

        Parameters
        ----------
        audio_data : np.ndarray
            Audio samples (mono or stereo)
        """
        raise NotImplementedError("Audio playback not implemented yet.")

    def stop(self):
        """
        Stop audio playback.
        """
        self._is_playing = False

    def is_playing(self) -> bool:
        """
        Return whether audio is currently playing.
        """
        return self._is_playing
