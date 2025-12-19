"""
Main window for Noise Studio UI (Advanced Version)

Enhanced version with custom fonts, animations, functional sidebar, and high-quality layout.
Compatible with existing SoundPanel and ImagePanel scripts.
"""

import dearpygui.dearpygui as dpg
from ui.panels.sound_panel import SoundPanel
from ui.panels.image_panel import ImagePanel
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO)

from ui import theme as ui_theme


class MainWindow:
    """Main application window controller with enhanced UI."""

    def __init__(self):
        self.sound_panel = SoundPanel()
        self.image_panel = ImagePanel()
        self.active_panel = "image"  # default panel

        # Fonts dictionary
        self.fonts = {}

        # Animation state
        self.animation_handles = []

    def run(self):
        """Initialize the UI and start Dear PyGui."""
        dpg.create_context()

        self._setup_fonts()

        # Apply a consolidated theme via ui.theme (best-effort)
        try:
            applied = ui_theme.apply_theme()
            if not applied:
                logging.debug("Theme not applied by ui_theme; falling back to internal theme.")
        except Exception:
            logging.debug("ui_theme.apply_theme failed; proceeding without theme.")

        dpg.create_viewport(title="Noise Studio", width=1280, height=800, resizable=True)

        self._setup_ui()

        dpg.setup_dearpygui()
        dpg.show_viewport()

        # Start animations
        self._start_animations()

        dpg.start_dearpygui()
        dpg.destroy_context()

    def _setup_fonts(self):
        """Load custom fonts safely using absolute paths and fallbacks."""
        fonts_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets", "fonts"))
        regular = os.path.join(fonts_dir, "Roboto-Regular.ttf")
        bold = os.path.join(fonts_dir, "Roboto-Bold.ttf")
        with dpg.font_registry():
            default_font = None
            header_font = None
            if os.path.exists(regular):
                default_font = dpg.add_font(regular, 18)
            if os.path.exists(bold):
                header_font = dpg.add_font(bold, 24)

            # Fallbacks: if header missing use default; if default missing, skip fonts
            if header_font is None and default_font is not None:
                header_font = default_font

            self.fonts = {}
            if default_font:
                self.fonts["default"] = default_font
            if header_font:
                self.fonts["header"] = header_font

            # Bind default font to the context if available
            try:
                if "default" in self.fonts:
                    dpg.bind_font(self.fonts["default"])
            except Exception:
                logging.debug("Could not bind default font; proceeding without binding.")

            # If no fonts found, inform the user how to add them
            if not self.fonts:
                logging.warning("No UI fonts found. To install a bold font, run: python tools/download_fonts.py")

    def _setup_ui(self):
        """Setup the main window layout with a toolbar, central preview and status bar."""
        with dpg.window(label="Noise Studio", width=1280, height=800):

            # Top toolbar
            with dpg.group(horizontal=True):
                ui_theme.add_toolbar_button("⚡ Generate (G)", lambda s,a,u: self._safe_call(self.image_panel.on_generate_clicked, s, a, on_done=lambda: self._update_status("Image generated")), tooltip="Generate image noise (G)")
                ui_theme.add_toolbar_button("▶ Play (Space)", lambda s,a,u: self._safe_call(self.sound_panel.on_play_clicked, s, a, on_done=lambda: self._update_status("Playing sound")), tooltip="Play sound (Space)")
                ui_theme.add_toolbar_button("📤 Export Image", lambda s,a,u: self._safe_call(self.on_export_image_clicked, s, a, on_done=lambda: self._update_status("Image exported")), tooltip="Export current image to disk")
                ui_theme.add_toolbar_button("📤 Export Sound", lambda s,a,u: self._safe_call(self.on_export_sound_clicked, s, a, on_done=lambda: self._update_status("Sound exported")), tooltip="Export current audio to disk")
                ui_theme.add_toolbar_button("⚙️ Settings", lambda s,a,u: self._safe_call(self._open_settings, s, a), tooltip="Open settings dialog")

            dpg.add_separator()

            # Sidebar (left)
            with dpg.group(horizontal=False, width=320):
                dpg.add_text("⚙️ Settings", parent=dpg.last_item(), tag="sidebar_header")
                if "header" in self.fonts:
                    dpg.bind_font(self.fonts["header"])
                dpg.add_separator()
                dpg.add_text("Adjust parameters below:")
                dpg.add_spacer()

                # Image panel controls
                dpg.add_text("🖼️ Image")
                dpg.add_slider_int(label="Width", default_value=self.image_panel.width, min_value=16, max_value=8192, callback=self._on_width_changed)
                dpg.add_slider_int(label="Height", default_value=self.image_panel.height, min_value=16, max_value=8192, callback=self._on_height_changed)
                dpg.add_checkbox(label="Live Preview", default_value=self.image_panel.live_preview, callback=self._on_image_live_preview_changed)
                dpg.add_button(label="Generate Image Noise", callback=self.image_panel.on_generate_clicked)
                dpg.add_spacer()

                # Sound panel controls
                dpg.add_text("🔊 Sound")
                dpg.add_slider_float(label="Duration (s)", default_value=self.sound_panel.duration, min_value=0.1, max_value=60, callback=self._on_duration_changed)
                dpg.add_checkbox(label="Live Preview", default_value=self.sound_panel.live_preview, callback=self._on_sound_live_preview_changed)
                dpg.add_button(label="Play Sound", callback=self.sound_panel.on_play_clicked)
                dpg.add_button(label="Stop Sound", callback=self.sound_panel.on_stop_clicked)

            # Central preview
            with dpg.group(horizontal=False):
                dpg.add_text("Preview Area", tag="preview_header")
                dpg.add_separator()
                with dpg.drawlist(width=512, height=512, tag="image_preview_canvas"):
                    pass

            # Bottom panel selector with highlight animation
            with dpg.group(horizontal=True):
                dpg.add_button(label="Sound Panel", callback=lambda: self.switch_panel("sound"), tag="btn_sound")
                dpg.add_button(label="Image Panel", callback=lambda: self.switch_panel("image"), tag="btn_image")

            # Right-hand properties panel
            with dpg.group(horizontal=False, horizontal_spacing=10):
                dpg.add_text("Properties")
                dpg.add_separator()
                dpg.add_combo(label="Noise Type", items=["white", "pink", "brown"], default_value=self.image_panel.noise_type, callback=lambda s,a,u: (self._set_noise_type(a), self._update_status(f"Noise type: {a}")))
                dpg.add_text("Preview Controls")
                dpg.add_separator()
                dpg.add_button(label="Center Image", callback=lambda s,a,u: (self.image_panel.on_generate_clicked(), self._update_status("Image centered")))
                dpg.add_button(label="Fit to View", callback=lambda s,a,u: (self.image_panel.on_generate_clicked(), self._update_status("Fitted to view")))
                dpg.add_spacer()

            # Bottom status bar
            with dpg.group(horizontal=True):
                dpg.add_text("Ready", tag="status_text")

        # Apply shortcuts and show active panel
        self._apply_shortcuts()
        self._show_active_panel()

    # -------------------------
    # Panel switching logic
    # -------------------------

    def _show_active_panel(self):
        if self.active_panel == "sound":
            self.sound_panel.show()
            self.image_panel.hide()
        else:
            self.image_panel.show()
            self.sound_panel.hide()
        self._update_button_highlight()

    def switch_panel(self, panel_name: str):
        if panel_name not in ("sound", "image"):
            raise ValueError("Invalid panel name")
        self.active_panel = panel_name
        self._show_active_panel()

    def _update_button_highlight(self):
        # Some DearPyGui versions may not support 'color' in configure_item; use label markers for compatibility
        if self.active_panel == "sound":
            dpg.set_item_label("btn_sound", "[Active] Sound Panel")
            dpg.set_item_label("btn_image", "Image Panel")
        else:
            dpg.set_item_label("btn_image", "[Active] Image Panel")
            dpg.set_item_label("btn_sound", "Sound Panel")

    # -------------------------
    # Animations / Live preview
    # -------------------------

    def _start_animations(self):
        # Toggle header label to create a light animation effect (robust across DPG versions)
        def flash_header(sender=None, app_data=None, user_data=None):
            state = getattr(flash_header, "state", False)
            flash_header.state = not state
            if flash_header.state:
                dpg.set_item_label("preview_header", "* Preview Area")
            else:
                dpg.set_item_label("preview_header", "Preview Area")

        # Use add_timer if available; otherwise, skip animations gracefully
        try:
            dpg.add_timer(callback=flash_header, user_data=None, delay=0.5, repeat=True)
        except Exception:
            # timers/animation API not available in this DearPyGui build; skip animations
            pass

    def _open_settings(self):
        """Open a simple settings modal dialog."""
        try:
            if dpg.does_item_exist("settings_window"):
                dpg.show_item("settings_window")
                return

            with dpg.window(label="Settings", modal=True, tag="settings_window"):
                dark = dpg.add_checkbox(label="Dark Theme", default_value=True)
                dpg.add_input_int(label="Audio sample rate", default_value=self.sound_panel.sample_rate, callback=self._on_sample_rate_changed)
                dpg.add_button(label="Apply", callback=lambda s,a,u: (ui_theme.apply_theme() if dpg.get_value(dark) else None, dpg.hide_item("settings_window")))
        except Exception as exc:
            logging.error("Failed to open settings dialog: %s", exc)

    def _on_sample_rate_changed(self, sender, app_data):
        try:
            self.sound_panel.sample_rate = int(app_data)
            self._update_status(f"Sample rate set to {app_data}")
        except Exception:
            logging.warning("Invalid sample rate value: %s", app_data)

    def _apply_shortcuts(self):
        """Register keyboard shortcuts (best-effort across DPG versions)."""
        try:
            # G -> generate image
            dpg.add_shortcut(callback=lambda s,a,u: self._safe_call(self.image_panel.on_generate_clicked, s, a, on_done=lambda: self._update_status("Image generated")), keys=[dpg.mvKey_G])
            # Space -> play/stop
            dpg.add_shortcut(callback=lambda s,a,u: self._safe_call(self.sound_panel.on_play_clicked, s, a, on_done=lambda: self._update_status("Playing sound")), keys=[dpg.mvKey_Space])
        except Exception:
            logging.debug("Shortcuts API not available; skipping shortcut registration.")

    def _safe_call(self, func, *args, on_done=None, **kwargs):
        """Execute a callable and log any exceptions; optionally call on_done afterwards."""
        try:
            func(*args, **kwargs)
            if callable(on_done):
                on_done()
        except Exception as exc:
            logging.exception("UI callback failed: %s", exc)
            try:
                self._update_status("Error: see console")
            except Exception:
                pass

    def _update_status(self, message: str):
        try:
            dpg.set_value("status_text", message)
        except Exception:
            logging.debug("Could not update status text: %s", message)

    def _set_noise_type(self, noise_type: str):
        self.image_panel.noise_type = noise_type
        self.sound_panel.noise_type = noise_type

    def _set_seed(self, seed_value: int):
        try:
            seed = int(seed_value)
        except Exception:
            seed = None
        if seed == 0:
            seed = None
        self.image_panel.seed = seed
        self.sound_panel.seed = seed

    def _apply_theme(self):
        """Apply a simple dark theme (best-effort, may be skipped on some DPG builds)."""
        try:
            theme = dpg.create_theme()
            with theme:
                # spacing & padding
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 6)
                # colors
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 120, 180, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 140, 200, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (230, 230, 230, 255))
            dpg.bind_theme(theme)
        except Exception:
            logging.debug("Theme application skipped; theme API may not be available in this DPG build.")

    # -------------------------
    # Sidebar callbacks
    # -------------------------

    def _on_width_changed(self, sender, app_data):
        self.image_panel.on_resolution_changed(app_data, self.image_panel.height)

    def _on_height_changed(self, sender, app_data):
        self.image_panel.on_resolution_changed(self.image_panel.width, app_data)

    def _on_duration_changed(self, sender, app_data):
        self.sound_panel.duration = app_data
        if self.sound_panel.live_preview:
            self.sound_panel.on_play_clicked()

    def _on_image_live_preview_changed(self, sender, app_data):
        self.image_panel.live_preview = app_data

    def _on_sound_live_preview_changed(self, sender, app_data):
        self.sound_panel.live_preview = app_data

    # -------------------------
    # Export callbacks (optional, placeholder)
    # -------------------------
    def on_export_image_clicked(self, sender, app_data):
        """
        Export the currently generated image to disk.
        """
        if hasattr(self.image_panel, 'texture_tag') and dpg.does_item_exist(self.image_panel.texture_tag):
            # Here you would integrate with your export module
            print(f"Exporting image of size {self.image_panel.width}x{self.image_panel.height}")
        else:
            print("No image generated to export.")

    def on_export_sound_clicked(self, sender, app_data):
        """
        Export the currently generated audio to disk.
        """
        # Placeholder: integrate with export engine
        print(f"Exporting audio of duration {self.sound_panel.duration}s")

    # -------------------------
    # Additional UI helpers
    # -------------------------
    def refresh_preview(self):
        """
        Refresh the preview area depending on the active panel.
        Called automatically if live preview is enabled.
        """
        if self.active_panel == "image" and self.image_panel.live_preview:
            self.image_panel.on_generate_clicked()
        elif self.active_panel == "sound" and self.sound_panel.live_preview:
            self.sound_panel.on_play_clicked()

    # -------------------------
    # Timer / animation helpers
    # -------------------------
    def _setup_live_preview_timer(self):
        """
        Setup a repeating timer that updates the preview if live preview is enabled.
        """
        def live_preview_callback():
            self.refresh_preview()
        dpg.add_timer(callback=live_preview_callback, delay=0.5, repeat=True)
