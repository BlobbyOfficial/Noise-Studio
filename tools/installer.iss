; Inno Setup script for Noise Studio

#define AppName "Noise Studio"
#define AppVersion "0.1"
#define AppExeName "NoiseStudio.exe"

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={pf}\{#AppName}
DisableProgramGroupPage=yes
OutputBaseFilename=NoiseStudio_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "{#GetCurrentDir()}\dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#GetCurrentDir()}\src\assets\*"; DestDir: "{app}\assets"; Flags: recursesubdirs createallsubdirs

[Dirs]
Name: "{userdocs}\NoiseStudio"
Name: "{userdocs}\NoiseStudio\output"
Name: "{userdocs}\NoiseStudio\output\images"
Name: "{userdocs}\NoiseStudio\output\sound"

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"

[Run]
; Run the app after installation
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent

[Setup]
LicenseFile=LICENSE

