# Screen Controller

**Remote Desktop Control System** - Educational Project for Learning Network Programming and Hardware Security

---

## What is this project?

This is an educational project that demonstrates:
- **Client-Server Communication** using Python sockets
- **Screen Capture and Streaming** using OpenCV
- **Remote Input Control** (mouse/keyboard) using PyAutoGUI
- **BadUSB Concept** using Arduino Pro Micro

---

## Project Files

| File | Description |
|------|-------------|
| `server_professional.py` | Server with GUI - runs on your computer, receives screen stream and sends commands |
| `client.ps1` | Client script - runs on target PC, captures screen and executes commands |
| `ProMicro.ino` | Arduino code - makes Pro Micro act as a keyboard to auto-run the client |
| `requirements.txt` | Python packages needed |

---

## How It Works

```
┌─────────────────┐                    ┌─────────────────┐
│   YOUR PC       │                    │   TARGET PC     │
│   (Server)      │◄───── WiFi ───────►│   (Client)      │
│                 │                    │                 │
│  - Shows screen │   Screen Stream    │  - Captures     │
│  - Send mouse   │◄──────────────────│    screen       │
│  - Send keys    │                    │  - Executes     │
│                 │   Commands         │    commands     │
│                 │──────────────────►│                 │
└─────────────────┘                    └─────────────────┘
```

---

## Requirements

### Software
- Python 3.7 or higher
- Arduino IDE (for Pro Micro)

### Python Packages
```bash
pip install opencv-python numpy pillow pyautogui
```

### Hardware (Optional)
- Pro Micro (ATmega32U4) - costs around $5

---

## Step-by-Step Usage

### Step 1: Find Your IP Address
```powershell
ipconfig
```
Look for "IPv4 Address" (example: `192.168.1.100`)

### Step 2: Update IP in Files
Edit `client.ps1` line 24:
```powershell
$serverIP = "YOUR_IP_HERE"
```

Edit `ProMicro.ino` line 20:
```cpp
const char* TARGET_IP = "YOUR_IP_HERE";
```

### Step 3: Open Firewall (Run as Admin)
```powershell
New-NetFirewallRule -DisplayName 'ScreenController' -Direction Inbound -LocalPort 5555 -Protocol TCP -Action Allow
```

### Step 4: Start Server
```bash
python server_professional.py
```

### Step 5: Run Client on Target PC
Option A: Run PowerShell script manually
Option B: Upload `ProMicro.ino` to Pro Micro and plug into target PC

---

## Code Explanation (For Lecturer)

### server_professional.py
- Creates TCP server socket on port 5555
- Receives JPEG images from client via pickle serialization
- Displays images in Tkinter GUI using OpenCV
- Sends mouse/keyboard commands back to client

### client.ps1
- Contains embedded Python code
- Uses `pyautogui.screenshot()` to capture screen
- Compresses with `cv2.imencode('.jpg', quality=80)`
- Sends data over socket with size header
- Receives commands and uses `pyautogui` to execute

### ProMicro.ino
- Uses Arduino `Keyboard.h` library
- Simulates keyboard to type PowerShell command
- Opens Run dialog with Win+R
- Types command to download and run client.ps1

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| Socket | Network communication (TCP) |
| OpenCV | Image processing and compression |
| Tkinter | GUI framework |
| PyAutoGUI | Screen capture and input simulation |
| Arduino | Keyboard emulation for BadUSB |

---

## Educational Purpose

This project teaches:
1. **Networking** - How TCP sockets work
2. **Image Processing** - Screen capture and JPEG compression
3. **GUI Development** - Building interfaces with Tkinter
4. **Hardware Hacking** - How BadUSB devices work
5. **Security Awareness** - Understanding attack vectors

---

## License

MIT License - Free for educational use

---

## Disclaimer

**For educational and authorized testing only.** 
Do not use on systems without permission.
