# Noise Studio

[![Download Installer](https://img.shields.io/badge/Download-Installer-blue?logo=windows&style=for-the-badge)](https://github.com/BlobbyOfficial/Noise-Studio/releases/download/v0.1-beta/NoiseStudio_Installer_v0.1-beta.exe)

Compact procedural image & audio noise generator.

---

## Quick start (Windows)

1. Download the **Installer** from the Releases page (recommended):
   - The installer (`NoiseStudio_Installer.exe`) will register the app and create the folder `Documents/NoiseStudio` with `output/images` and `output/sound` subfolders for exported assets.

2. Or run the portable single-file executable:
   - Download `dist/NoiseStudio.exe` from the latest release and run it directly.

> Tip: prefer the Installer for a smoother experience; the portable EXE is fine for testing.

---

## From source (developers)

1. Create and activate a virtual environment (Windows example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app:

```powershell
python -m src.app
# or
python src\app.py
```

3. Build a Windows executable locally:

```powershell
tools\build_exe.bat
```

- The helper will create `dist/NoiseStudio.exe` using PyInstaller. If Inno Setup is installed on the machine, `tools\installer.iss` can be used to create an installer `NoiseStudio_Installer.exe`.

---

## Releases & Assets

- When publishing a release (tag: `v0.1-beta`, mark as **Pre-release**), attach a Windows installer `.exe` for the best user experience. If no installer is available, attach the `dist/NoiseStudio.exe` portable executable.
- The GitHub username for this project is **blobbyofficial** (links and site assume this account).

---

## Website

- The repository includes a simple `index.html` that fetches and renders the README from GitHub at runtime. The site points users to the Releases page for downloads and provides a quick summary of the project.

---

## Tests & CI

- Run the test suite with:

```bash
pytest
```

- GitHub Actions workflows (`.github/workflows/`) run tests on pushes/PRs and can produce Windows builds on tagged releases.

---

## Reporting bugs & contributing

- Please open issues on the repo (include OS, Python version, steps to reproduce, and logs if available).
- Pull requests are welcome — keep changes focused and include tests where applicable.

---

## License

This project includes a `LICENSE` file — see it for license details.

---

*Maintained by blobbyofficial — thanks for testing the beta!*
