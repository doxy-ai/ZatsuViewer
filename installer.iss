#define MyAppName "ZatsuDachi"
#define MyAppVersion "0.0.1"
#define PythonURL "https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"
#define ZipURL "https://github.com/doxy-ai/ZatsuDachi/archive/refs/heads/master.zip"

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
Filename: "{app}\pythonFinder.bat"; WorkingDir: "{app}"; Parameters: "-m pip install colour flask flask_socketio tk requests"; Description: "Install Needed Python Dependencies (Recommended)"; Flags: postinstall runascurrentuser shellexec waituntilterminated;
Filename: "{app}\pythonFinder.bat"; WorkingDir: "{app}"; Parameters: "downloadPlugin.py twitch"; Description: "Install Twitch Support"; Flags: postinstall runascurrentuser unchecked shellexec waituntilterminated; Check: ShouldGetTwitch
Filename: "{app}\pythonFinder.bat"; WorkingDir: "{app}"; Parameters: "downloadPlugin.py youtube"; Description: "Install Youtube Support"; Flags: postinstall runascurrentuser unchecked shellexec waituntilterminated; Check: ShouldGetYoutube
Filename: "{app}\pythonFinder.bat"; WorkingDir: "{app}"; Parameters: "downloadPlugin.py vstream"; Description: "Install Vstream Support"; Flags: postinstall runascurrentuser unchecked shellexec waituntilterminated; Check: ShouldGetVstream

[Icons]
; Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppName}.exe"
Name: "{commonprograms}\ZatsuDachi";  WorkingDir: "{app}"; Filename: "{app}\pythonFinder.bat"; Parameters: "zatsu.py"; IconFilename: "{app}\resources\icon.ico"; Comment: "Run Zatsu.py"

[Code]
var
  PythonInstalled: Boolean;
  PythonInstallerPath: string;
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

procedure InitializeWizard;
begin
  PythonInstalled := RegKeyExists(HKLM, 'Software\Python\PythonCore\3.10\InstallPath');
  DownloadPage := CreateDownloadPage(SetupMessage(msgWizardPreparing), SetupMessage(msgPreparingDesc), @OnDownloadProgress);
end;

function ShouldInstallPython: Boolean;
begin
  Result := not PythonInstalled;
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


function NextButtonClick(CurPageID: Integer): Boolean;
begin
  if CurPageID = wpReady then begin
    if PythonInstalled = False then
    begin
      DownloadPage.Clear;
      DownloadPage.Add('{#PythonURL}', 'python-3.10.11-amd64.exe', '');
      DownloadPage.Show;
      try
        try
          DownloadPage.Download;
          Result := True;
        except
          SuppressibleMsgBox(AddPeriod(GetExceptionMessage), mbCriticalError, MB_OK, IDOK);
          Result := False;
        end;
      finally
        DownloadPage.Hide;
      end;
    end;
  end else
    Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssInstall then
  begin
    if ShouldInstallPython then
    begin
      PythonInstallerPath := ExpandConstant('{tmp}\python-3.10.0-amd64.exe');
      if FileExists(PythonInstallerPath) then
      begin
        Exec(PythonInstallerPath, '', '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
        if ResultCode = 0 then
          PythonInstalled := True;
      end
      else
      begin
        MsgBox('Python found so not installing!', mbInformation, MB_OK);
      end;
    end;
  end;
end;