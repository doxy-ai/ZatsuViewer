#define MyAppName "ZatsuDachi"
#define MyAppVersion "0.0.1"
#define PythonURL "https://python.org/downloads/release/python-31011/"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppName}.exe
SetupIconFile=resources\icon.ico
PrivilegesRequired=admin
OutputDir=Output
Compression=lzma2
SolidCompression=yes

[Files]
Source: "*.*"; Excludes: "installer.iss,.git,*__pycache__*"; DestDir: "{app}"; Flags:replacesameversion recursesubdirs

[Run]
Filename: {#PythonURL}; Description: "Open Python Download Page (rerun installer after installing Python)"; Flags: postinstall runascurrentuser shellexec waituntilterminated unchecked; 
Filename: "{app}\pythonFinder.bat"; WorkingDir: "{app}"; Parameters: "-m pip install colour flask flask_socketio tk requests"; Description: "Install Needed Python Dependencies (Recommended)"; Flags: postinstall runascurrentuser shellexec waituntilterminated;
Filename: "{app}\pythonFinder.bat"; WorkingDir: "{app}"; Parameters: "downloadPlugin.py twitch"; Description: "Install Twitch Support"; Flags: postinstall runascurrentuser unchecked shellexec waituntilterminated; Check: ShouldGetTwitch
Filename: "{app}\pythonFinder.bat"; WorkingDir: "{app}"; Parameters: "downloadPlugin.py youtube"; Description: "Install Youtube Support"; Flags: postinstall runascurrentuser unchecked shellexec waituntilterminated; Check: ShouldGetYoutube
Filename: "{app}\pythonFinder.bat"; WorkingDir: "{app}"; Parameters: "downloadPlugin.py vstream"; Description: "Install Vstream Support"; Flags: postinstall runascurrentuser unchecked shellexec waituntilterminated; Check: ShouldGetVstream

[Icons]
; Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppName}.exe"
Name: "{commonprograms}\ZatsuDachi";  WorkingDir: "{app}"; Filename: "{app}\pythonFinder.bat"; Parameters: "zatsu.py"; IconFilename: "{app}\resources\icon.ico"; Comment: "Run Zatsu.py"

[Code]
var
  ZipFilePath: string;
  DownloadPage: TDownloadWizardPage;

const
  SHCONTCH_NOPROGRESSBOX = 4;
  SHCONTCH_RESPONDYESTOALL = 16;

function OnDownloadProgress(const Url, FileName: String; const Progress, ProgressMax: Int64): Boolean;
begin
  if Progress = ProgressMax then
    Log(Format('Successfully downloaded file to {tmp}: %s', [FileName]));
  Result := True;
end;

function ShouldGetTwitch: Boolean;
begin
  Result := True;
end;

function ShouldGetYoutube: Boolean;
begin
  Result := True;
end;

function ShouldGetVstream: Boolean;
begin
  Result := True;
end;