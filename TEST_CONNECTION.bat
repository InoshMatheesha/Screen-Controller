@echo off
echo ========================================
echo TESTING SERVER CONNECTION
echo ========================================
echo.
echo Your Server IP: 172.28.1.78
echo Port: 5555
echo.
echo Step 1: Testing if port 5555 is open...
powershell -Command "Test-NetConnection -ComputerName 172.28.1.78 -Port 5555"
echo.
echo Step 2: Checking firewall rules...
powershell -Command "Get-NetFirewallRule | Where-Object {$_.LocalPort -eq 5555 -and $_.Direction -eq 'Inbound'} | Select-Object Name, Enabled, Action"
echo.
echo ========================================
echo If port is NOT open, run: SETUP_FIREWALL.bat (as admin)
echo ========================================
pause
