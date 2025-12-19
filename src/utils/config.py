"""Simple config and paths helper.

Provides:
- `get_app_dirs()` -> returns root data path (Documents/NoiseStudio) and subfolders
- `load_settings()` / `save_settings()` -> read/write a small JSON config
- Defaults live_preview: True, sample_rate: 44100, theme: dark
"""
import json
from pathlib import Path
from typing import Dict, Any

DEFAULT_SETTINGS = {
    "live_preview": True,
    "sample_rate": 44100,
    "theme": "dark"
}


def get_documents_dir() -> Path:
    home = Path.home()
    # Windows typical Documents path
    docs = home / "Documents"
    appdir = docs / "NoiseStudio"
    return appdir


def get_app_dirs() -> Dict[str, Path]:
    base = get_documents_dir()
    images = base / "output" / "images"
    sounds = base / "output" / "sound"
    cfg = base / "config.json"
    return {"base": base, "images": images, "sounds": sounds, "config": cfg}


def ensure_app_dirs():
    dirs = get_app_dirs()
    dirs["base"].mkdir(parents=True, exist_ok=True)
    dirs["images"].mkdir(parents=True, exist_ok=True)
    dirs["sounds"].mkdir(parents=True, exist_ok=True)


def load_settings() -> Dict[str, Any]:
    p = get_app_dirs()["config"]
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()


def save_settings(settings: Dict[str, Any]):
    ensure_app_dirs()
    p = get_app_dirs()["config"]
    p.write_text(json.dumps(settings, indent=2))
