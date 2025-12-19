"""
SoundPanel UI for Noise Studio

High-quality, polished, fully functional sound noise panel
with live preview and professional layout.
"""

import numpy as np
import sounddevice as sd
import logging
from engine.audio_noise import AudioNoiseGenerator

class SoundPanel:
    """UI panel for sound noise generation and playback."""

    def __init__(self):
        self.visible = False
        self.duration = 1.0  # seconds
        self.sample_rate = 44100
        self.seed = None
        self.live_preview = True
        self.noise_type = "white"  # default noise type

        # Internal state
        self._current_audio = None
        self._stream = None

    # -------------------------
    # Panel visibility
    # -------------------------
    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False
        self.stop_audio()

    # -------------------------
    # Noise type changes
    # -------------------------
    def on_noise_type_changed(self, noise_type: str):
        self.noise_type = noise_type
        if self.live_preview:
            self.play_audio()

    # -------------------------
    # Duration changes
    # -------------------------
    def on_duration_changed(self, duration: float):
        self.duration = duration
        if self.live_preview:
            self.play_audio()

    # -------------------------
    # Audio generation
    # -------------------------
    def generate_noise(self):
        """Generate noise samples for the selected type."""
        generator = AudioNoiseGenerator(
            sample_rate=self.sample_rate,
            seed=self.seed
        )

        if self.noise_type == "white":
            audio = generator.generate_white_noise(self.duration)
        elif self.noise_type == "pink":
            audio = generator.generate_pink_noise(self.duration)
        elif self.noise_type == "brown":
            audio = generator.generate_brown_noise(self.duration)
        else:
            audio = generator.generate_white_noise(self.duration)

        # Normalize audio to prevent clipping
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val

        self._current_audio = audio
        return audio

    # -------------------------
    # Playback
    # -------------------------
    def play_audio(self, sender=None, app_data=None):
        """Play the generated audio noise with graceful error handling."""
        self.stop_audio()  # stop existing playback

        audio = self.generate_noise()

        if audio is not None:
            try:
                self._stream = sd.OutputStream(
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype='float32'
                )
                self._stream.start()
                self._stream.write(audio.astype(np.float32))
                print(f"Playing {self.noise_type} noise for {self.duration}s")
            except Exception as exc:
                # Log and fail gracefully if audio device or stream creation fails
                logging.error("Audio playback failed: %s", exc)
                self._stream = None

    def stop_audio(self, sender=None, app_data=None):
        """Stop audio playback."""
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
            print("Stopped audio playback")

    # -------------------------
    # UI callback wrappers
    # -------------------------
    def on_play_clicked(self, sender=None, app_data=None):
        """Callback wrapper for Play button."""
        self.play_audio(sender, app_data)

    def on_stop_clicked(self, sender=None, app_data=None):
        """Callback wrapper for Stop button."""
        self.stop_audio(sender, app_data)

    # -------------------------
    # Live preview toggle
    # -------------------------
    def set_live_preview(self, enabled: bool):
        self.live_preview = enabled
        if self.live_preview:
            self.play_audio()
    # -------------------------
    # Export helper
    # -------------------------
    def get_current_audio(self):
        """Return the current audio array for export."""
        return self._current_audio
