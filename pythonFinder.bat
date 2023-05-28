@echo off

REM Search for Python executable in the system path
for /f "delims=" %%I in ('where python') do (
    set PYTHON_EXECUTABLE=%%I
    goto :RunPythonScript
)

REM If Python executable is not found, display an error message
echo Python is not installed or not found in the system path.
pause
exit /b

:RunPythonScript
REM Execute the Python script with the specified arguments
@REM echo "%PYTHON_EXECUTABLE%"
echo %*
"%PYTHON_EXECUTABLE%" %*