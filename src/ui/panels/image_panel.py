"""
ImagePanel UI for Noise Studio

High-quality, polished, fully functional image noise panel
with live preview and professional layout.
"""

import dearpygui.dearpygui as dpg
import numpy as np
from engine.image_noise import ImageNoiseGenerator

class ImagePanel:
    """UI panel for image noise generation and preview."""

    def __init__(self):
        self.visible = False
        self.width = 512
        self.height = 512
        self.seed = None
        self.live_preview = True
        self.noise_type = "white"  # default noise type

        # Internal texture tag for Dear PyGui canvas
        self.texture_tag = "image_preview_texture"

        # Currently generated image array (for export)
        self.current_image = None

    # -------------------------
    # Panel visibility
    # -------------------------
    def show(self):
        self.visible = True
        # The sidebar in MainWindow manages controls, so no GUI creation here
        # Could add additional panel-specific popups or overlays later

    def hide(self):
        self.visible = False

    # -------------------------
    # Resolution changes
    # -------------------------
    def on_resolution_changed(self, width: int, height: int):
        self.width = width
        self.height = height
        if self.live_preview:
            self.on_generate_clicked()

    # -------------------------
    # Noise type changes
    # -------------------------
    def on_noise_type_changed(self, noise_type: str):
        self.noise_type = noise_type
        if self.live_preview:
            self.on_generate_clicked()

    # -------------------------
    # Noise generation
    # -------------------------
    def on_generate_clicked(self, sender=None, app_data=None):
        """Generate noise and update the preview canvas."""
        # Step 1: Generate noise using the engine
        generator = ImageNoiseGenerator(
            width=self.width,
            height=self.height,
            seed=self.seed
        )

        if self.noise_type == "white":
            noise = generator.generate_white_noise()
        elif self.noise_type == "pink":
            noise = generator.generate_pink_noise()
        elif self.noise_type == "brown":
            noise = generator.generate_brown_noise()
        else:
            noise = generator.generate_white_noise()

        self.current_image = noise  # save for export

        # Step 2: Convert to 0-255 uint8 format
        image_data = np.clip(noise * 255, 0, 255).astype(np.uint8)

        # Convert grayscale to RGB
        if len(image_data.shape) == 2:
            image_data = np.stack([image_data] * 3, axis=-1)

        # Flatten for Dear PyGui (normalized to 0-1)
        flat_image = image_data.flatten() / 255.0

        # Step 3: Update Dear PyGui texture
        if dpg.does_item_exist(self.texture_tag):
            dpg.delete_item(self.texture_tag)

        with dpg.texture_registry(show=False):
            dpg.add_static_texture(
                width=self.width,
                height=self.height,
                default_value=flat_image,
                tag=self.texture_tag
            )

        # Step 4: Draw image on canvas
        if dpg.does_item_exist("image_preview_canvas"):
            # Clear previous canvas content
            dpg.delete_item("image_preview_canvas", children_only=True)
            # Draw image directly into the existing drawlist
            dpg.draw_image(
                self.texture_tag,
                pmin=(0, 0),
                pmax=(self.width, self.height),
                parent="image_preview_canvas"
            )

    # -------------------------
    # Live preview toggling
    # -------------------------
    def set_live_preview(self, enabled: bool):
        self.live_preview = enabled
        if self.live_preview:
            self.on_generate_clicked()

    # -------------------------
    # Export helper
    # -------------------------
    def get_current_image(self):
        """Return the currently generated image array for export."""
        return self.current_image
