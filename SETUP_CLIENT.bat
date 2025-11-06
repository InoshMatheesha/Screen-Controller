@echo off
color 0B
cls
echo.
echo ================================================
echo   CLIENT SETUP - Run on 2nd Laptop
echo ================================================
echo.
echo This will automatically install all required
echo packages on the victim/client laptop.
echo.
echo Requirements:
echo   - Python must be installed
echo   - Internet connection
echo.
pause

REM Run setup script
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0SETUP_CLIENT.ps1"

pause
