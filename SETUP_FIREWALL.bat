@echo off
echo ========================================
echo FIREWALL SETUP - RUN AS ADMINISTRATOR
echo ========================================
echo.
echo This will allow incoming connections on port 5555
echo.

net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running as Administrator
    echo.
    echo Creating firewall rule...
    powershell -Command "New-NetFirewallRule -DisplayName 'RemoteControl-5555' -Direction Inbound -LocalPort 5555 -Protocol TCP -Action Allow"
    echo.
    echo [DONE] Firewall rule created!
    echo.
) else (
    echo [ERROR] NOT running as Administrator!
    echo.
    echo Right-click this file and select "Run as administrator"
    echo.
)

pause
