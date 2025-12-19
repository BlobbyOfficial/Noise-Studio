"""
Preview manager module.

Coordinates live preview generation for both
audio and image noise.
"""

import threading
from typing import Callable, Optional


class PreviewManager:
    """
    Manages live preview updates and throttling.
    """

    def __init__(self):
        self.live_preview_enabled = True
        self._lock = threading.Lock()
        self._preview_thread: Optional[threading.Thread] = None

    def set_live_preview(self, enabled: bool):
        """
        Enable or disable live preview.
        """
        self.live_preview_enabled = enabled

    def request_preview_update(
        self,
        preview_callback: Callable[[], None],
    ):
        """
        Request a preview update.

        The callback should generate preview-quality data only.
        """
        if not self.live_preview_enabled:
            return

        if self._preview_thread and self._preview_thread.is_alive():
            return  # prevent stacking updates

        self._preview_thread = threading.Thread(
            target=self._run_preview,
            args=(preview_callback,),
            daemon=True,
        )
        self._preview_thread.start()

    def _run_preview(self, callback: Callable[[], None]):
        """
        Internal preview execution.
        """
        with self._lock:
            callback()
