@echo off
echo ========================================
echo STARTING CLIENT - CONNECTING TO SERVER
echo ========================================
echo.

REM Read IP from LAST_IP.txt
set /p SERVER_IP=<LAST_IP.txt

echo Connecting to: %SERVER_IP%:5555
echo.
echo This window will show connection status...
echo.

python client_control.py --server %SERVER_IP% --port 5555 --no-hide

pause
