@echo off
echo ============================================
echo   FIREWALL SETUP - RUN AS ADMINISTRATOR
echo ============================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running as Administrator
    echo.
    echo Opening firewall ports 5555 and 8000...
    echo.
    
    REM Create firewall rules
    powershell -Command "New-NetFirewallRule -DisplayName 'RemoteControl-Port5555' -Direction Inbound -LocalPort 5555 -Protocol TCP -Action Allow -ErrorAction SilentlyContinue"
    powershell -Command "New-NetFirewallRule -DisplayName 'RemoteControl-Port8000' -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow -ErrorAction SilentlyContinue"
    
    echo.
    echo [SUCCESS] Firewall configured!
    echo Port 5555: Control Server
    echo Port 8000: Web Server
    echo.
) else (
    echo [ERROR] NOT running as Administrator!
    echo.
    echo Right-click this file and select "Run as administrator"
    echo.
)

pause
