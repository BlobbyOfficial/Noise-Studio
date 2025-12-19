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

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent
