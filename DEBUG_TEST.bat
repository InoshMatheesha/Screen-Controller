@echo off
color 0E
cls
echo.
echo ================================================
echo   DEBUG MODE - Test Client Connection
echo ================================================
echo.
echo This will show detailed error messages
echo and won't close automatically.
echo.
echo Make sure your server is running first!
echo.
pause

REM Run debug script
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0DEBUG_CLIENT.ps1"

pause
