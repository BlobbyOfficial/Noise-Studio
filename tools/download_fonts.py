"""Download optional fonts (Roboto Bold) into src/assets/fonts if missing.

Usage:
    python tools/download_fonts.py

This script is best-effort and will not overwrite an existing file.
"""
import os
import sys
import urllib.request

FONT_URL = "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Bold.ttf"

ROOT = os.path.dirname(os.path.dirname(__file__))  # project root
DEST_DIR = os.path.join(ROOT, "src", "assets", "fonts")
DEST_FILE = os.path.join(DEST_DIR, "Roboto-Bold.ttf")


def download_font(url=FONT_URL, dest=DEST_FILE):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest):
        print(f"Font already exists at {dest}")
        return True
    try:
        print(f"Downloading font from {url}...")
        with urllib.request.urlopen(url) as response, open(dest, "wb") as out_file:
            out_file.write(response.read())
        print(f"Saved font to {dest}")
        return True
    except Exception as e:
        print(f"Failed to download font: {e}")
        return False


if __name__ == "__main__":
    success = download_font()
    sys.exit(0 if success else 1)
