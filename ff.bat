@echo off
setlocal

rem Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"

rem Run the Python script with all arguments passed to this script
python "%SCRIPT_DIR%ff.py" %* 