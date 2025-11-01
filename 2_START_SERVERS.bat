@echo off
color 0A
cls
echo.
echo ================================================
echo   STARTING REMOTE CONTROL SERVERS
echo ================================================
echo.
echo Your IP: 172.28.1.78
echo Control Port: 5555
echo Web Server Port: 8000
echo.
echo ================================================
echo.

REM Get the directory where this bat file is located
set SCRIPT_DIR=%~dp0

REM Start web server silently in background
echo [1/2] Starting Web Server (port 8000) - Hidden...
start /B pythonw -m http.server 8000 >nul 2>&1

REM Wait a moment
timeout /t 1 /nobreak >nul

REM Start control GUI
echo [2/2] Starting Control Server GUI...
echo.
echo ================================================
echo   GUI LAUNCHING
echo ================================================
echo.
echo Web Server: Running in background (hidden)
echo Control GUI: Opening now...
echo.
echo Close the GUI to stop all servers.
echo ================================================
echo.

REM Start GUI and wait for it to close
python "%SCRIPT_DIR%server_professional.py"

REM When GUI closes, kill web server
echo.
echo Stopping background web server...
taskkill /F /IM pythonw.exe >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq http.server*" >nul 2>&1

echo Servers stopped.
timeout /t 2 >nul
