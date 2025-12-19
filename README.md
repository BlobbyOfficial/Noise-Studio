Noise Studio
============

Procedural image and audio noise generator.

Quick setup
-----------
- Create and activate the virtual environment (if you haven't already).
- Install dependencies:

```bash
pip install -r requirements.txt
```

Optional: download a bold font used by the UI headers:

```bash
python tools/download_fonts.py
```

Build a Windows executable locally
---------------------------------
- Create and activate a virtualenv on Windows.
- Run the helper: `tools\build_exe.bat` to produce `dist\NoiseStudio.exe` (and optionally an installer if Inno Setup is installed).

CI / Automated installer builds
------------------------------
- A GitHub Actions workflow is included (`.github/workflows/build_windows.yml`) that will run on a tag push (v*) or manually.
- The workflow uses PyInstaller to build a single-file executable and attempts to run Inno Setup to build an installer.

Create a GitHub repository and publish a release
------------------------------------------------
1. Create a new repository on GitHub (https://github.com/new) named `noise-studio`, or run:

```bash
# replace USERNAME with your GitHub username
git remote add origin git@github.com:USERNAME/noise-studio.git
git branch -M main
git push -u origin main
```

2. Tag a release to trigger the Windows build & release workflow:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The release workflow will attempt to build the exe and upload it as a release asset.

Testing
-------
Run:

```bash
pytest
```

CI
--
A GitHub Actions workflow runs tests on push and PR automatically (`.github/workflows/ci.yml`).
