"""Theme utilities for Noise Studio UI.

Provides a best-effort theme application compatible with multiple DearPyGui builds
and convenience helpers for adding toolbar buttons with tooltips.
"""
import logging

try:
    import dearpygui.dearpygui as dpg
except Exception:
    dpg = None


def apply_theme() -> bool:
    """Apply a simple dark theme. Returns True if applied, False otherwise."""
    if dpg is None:
        logging.debug("DearPyGui not available; skipping theme application.")
        return False
    try:
        theme = dpg.create_theme()
        with theme:
            # spacing & padding
            try:
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 10)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 8)
            except Exception:
                logging.debug("Theme style API missing; skipping style definitions.")

            # colors (best effort)
            try:
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (27, 27, 27, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (64, 128, 192, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 150, 220, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (39, 39, 39, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 220, 220, 255))
            except Exception:
                logging.debug("Theme color API missing; skipping color definitions.")

        dpg.bind_theme(theme)
        return True
    except Exception as exc:
        logging.debug("Theme application failed: %s", exc)
        return False


def add_toolbar_button(label: str, callback, tooltip: str | None = None, parent=None):
    """Add a toolbar button and an optional tooltip.

    Returns the item id.
    """
    if dpg is None:
        return None
    try:
        if parent is None:
            btn = dpg.add_button(label=label, callback=callback)
        else:
            btn = dpg.add_button(label=label, callback=callback, parent=parent)
        if tooltip:
            # prefer tooltip context if available
            try:
                with dpg.tooltip(btn):
                    dpg.add_text(tooltip)
            except Exception:
                # Silently continue if tooltip API isn't available
                pass
        return btn
    except Exception:
        # Best-effort fallback: try without parent
        try:
            return dpg.add_button(label=label, callback=callback)
        except Exception:
            logging.debug("Failed to add toolbar button: %s", label)
            raise

