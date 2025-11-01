@echo off
echo ========================================
echo STARTING SERVER ON 172.28.1.78:5555
echo ========================================
echo.
echo Server is starting...
echo Keep this window open!
echo.
echo On the second laptop (client), run:
echo    python client_control.py --server 172.28.1.78 --port 5555
echo.
echo Or double-click: START_CLIENT.bat
echo ========================================
echo.

python server_professional.py

pause
