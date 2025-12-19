@echo off
REM Build the Windows single-file executable and optionally create an installer via Inno Setup.
REM Usage: Open an elevated Developer PowerShell/CMD, activate your virtualenv, then run this script.

REM Move to project root (parent of /tools)
cd /d %~dp0..
echo Current directory: %cd%

if not exist .venv\Scripts\activate (
  echo Please create and activate the virtual environment first (python -m venv .venv)
  echo Activating the global Python environment as fallback.
) else (
  call .venv\Scripts\activate
)

python -m pip install --upgrade pip
pip install pyinstaller==5.11

echo.
echo Cleaning previous builds...
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q *.spec

echo.
echo Building single-file executable with PyInstaller...
REM Add assets into the bundle; on Windows the separator is a semicolon.
pyinstaller --noconfirm --onefile --windowed --add-data "src\assets;assets" --name "NoiseStudio" src\app.py
if ERRORLEVEL 1 exit /b %ERRORLEVEL%

if exist dist\NoiseStudio.exe (
  echo Built dist\NoiseStudio.exe
  REM Try to create an installer using Inno Setup (ISCC.exe expected in standard install location)
  if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
    "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" tools\installer.iss
    echo Installer created.
  ) else (
    echo Inno Setup not found. To create an installer, install Inno Setup and run tools\installer.iss
  )
) else (
  echo Build failed: dist\NoiseStudio.exe not found.
)

pause
