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

        # Whether we are running inside the UI (MainWindow will set this)
        self.ui_enabled = False

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
        # Auto-save generated audio
        try:
            from utils.config import get_app_dirs
            from scipy.io.wavfile import write as wav_write
            from datetime import datetime
            dirs = get_app_dirs()
            fname = dirs["sounds"] / f"sound_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            # normalize to int16
            maxv = max(1.0, np.max(np.abs(audio)))
            wav = (audio / maxv * 32767).astype('int16')
            wav_write(str(fname), self.sample_rate, wav)
            print(f"Saved generated audio to {fname}")
        except Exception as exc:
            print("Failed to auto-save audio:", exc)
        return audio

    # -------------------------
    # Playback
    # -------------------------
    def play_audio(self, sender=None, app_data=None):
        """Play the generated audio noise with graceful error handling and autosave."""
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
                # Play in a non-blocking way: write may block, but wrapping in try-catch
                self._stream.write(audio.astype(np.float32))
                print(f"Playing {self.noise_type} noise for {self.duration}s")
            except Exception as exc:
                # Log and fail gracefully if audio device or stream creation fails
                logging.error("Audio playback failed: %s", exc)
                self._stream = None

        # Non-GUI environments: nothing else to do here; GUI-specific actions happen in the UI code.
        try:
            pass
        except Exception:
            pass

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

    def save_to(self, path):
        """Save the last generated audio array to `path` in WAV format."""
        if self._current_audio is None:
            raise RuntimeError("No audio generated")
        try:
            from scipy.io.wavfile import write as wav_write
            maxv = max(1.0, np.max(np.abs(self._current_audio)))
            wav = (self._current_audio / maxv * 32767).astype('int16')
            wav_write(path, self.sample_rate, wav)
        except Exception:
            raise

