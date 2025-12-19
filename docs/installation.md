# Installation

## Windows
1. Build locally using the helper (requires Python and optionally Inno Setup):

```powershell
tools\build_exe.bat
```

2. That script will create `dist\NoiseStudio.exe`.
3. If Inno Setup (ISCC) is installed, it will also produce an installer that creates the Documents folders for you and copy assets.

## Using the release
If you download the installer, it will create `C:\Users\<you>\Documents\NoiseStudio\output\images` and `...\sound` and save generated files there automatically.
