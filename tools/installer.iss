; Inno Setup script for Noise Studio

#define AppName "Noise Studio"
#define AppVersion "0.1-beta"
#define AppExeName "NoiseStudio.exe"
#define AppPublisher "Blobby Official"
#define AppURL "https://github.com/blobbyofficial/noise-studio"

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
DefaultDirName={pf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=no
OutputBaseFilename=NoiseStudio_Installer
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

; Include the built single-file EXE and bundled assets
[Files]
Source: "{#GetCurrentDir()}\dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#GetCurrentDir()}\src\assets\*"; DestDir: "{app}\assets"; Flags: recursesubdirs createallsubdirs
Source: "{#GetCurrentDir()}\README.md"; DestDir: "{app}"; Flags: isreadme

[Dirs]
Name: "{userdocs}\NoiseStudio"
Name: "{userdocs}\NoiseStudio\output"
Name: "{userdocs}\NoiseStudio\output\images"
Name: "{userdocs}\NoiseStudio\output\sound"

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent

[Setup]
LicenseFile=LICENSE

;-----------------------------
; Optional: add uninstallation cleanup
[UninstallDelete]
Type: filesandordirs; Name: "{userdocs}\NoiseStudio\output"

