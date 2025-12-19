"""
Preset handling module.

Responsible for saving and loading noise presets
to and from disk.
"""

import json
from pathlib import Path
from typing import Dict, Any


PRESET_SCHEMA_VERSION = 1


def save_preset(
    preset_data: Dict[str, Any],
    file_path: Path,
):
    """
    Save a preset to disk as JSON.
    """
    data = {
        "schema_version": PRESET_SCHEMA_VERSION,
        "preset": preset_data,
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_preset(file_path: Path) -> Dict[str, Any]:
    """
    Load a preset from disk.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "schema_version" not in data:
        raise ValueError("Invalid preset file (missing schema version).")

    return data["preset"]
