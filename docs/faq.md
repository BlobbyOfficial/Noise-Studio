# FAQ

Q: Why is my audio not playing?
A: Noise Studio uses your system audio device. If playback fails, check that no other app has exclusive access and that your drivers are up to date. Errors are logged to console.

Q: Where are my generated files?
A: Generated images/audio are saved into your Documents folder: `Documents/NoiseStudio/output/*`.

Q: How do I make the installer?
A: Use `tools\build_exe.bat` on Windows with Inno Setup installed to produce an installer. The CI includes a workflow that creates a release on tag pushes.
