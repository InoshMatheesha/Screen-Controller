# Screen Share

Simple screen sharing project using Python sockets.

---

## What It Does

One computer shares its screen to another computer over WiFi.

```
  CLIENT PC                         SERVER PC
  (shares screen)                   (views screen)
       |                                 |
       |  1. Capture screenshot          |
       |  2. Compress as JPEG            |
       |  3. Send over network --------> |
       |                                 |  4. Receive image
       |                                 |  5. Display in window
```

---

## Files

| File | What it does |
|------|-------------|
| `server.py` | Receives and displays the screen (run on YOUR computer) |
| `client.py` | Captures and sends screen (run on TARGET computer) |
| `ProMicro.ino` | Arduino code to auto-run the client |
| `client.ps1` | PowerShell version of client |

---

## How to Use

### Step 1: Install Python packages
```
pip install opencv-python numpy pyautogui
```

### Step 2: Find your IP address
```
ipconfig
```
Look for IPv4 Address (example: 192.168.1.100)

### Step 3: Edit client.py
Change line 12:
```python
SERVER_IP = "YOUR_IP_HERE"
```

### Step 4: Run server on your PC
```
python server.py
```

### Step 5: Run client on target PC
```
python client.py
```

Now you can see the target PC's screen!

---

## Code Explanation

### server.py (70 lines)
1. Creates TCP socket on port 5555
2. Waits for client to connect
3. Receives JPEG image data
4. Decodes and displays using OpenCV

### client.py (50 lines)
1. Connects to server IP
2. Captures screen using `pyautogui.screenshot()`
3. Compresses to JPEG using `cv2.imencode()`
4. Sends data with size header

### ProMicro.ino (40 lines)
1. Uses Arduino Keyboard library
2. Simulates keyboard typing
3. Opens Run dialog (Win+R)
4. Types command to run client

---

## Technologies

- **Python** - Programming language
- **Socket** - Network communication
- **OpenCV** - Image processing
- **PyAutoGUI** - Screen capture
- **Arduino** - Hardware keyboard emulation

---

## For Educational Use Only
