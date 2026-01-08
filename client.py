"""
Simple Screen Share Client
- Captures screen
- Sends to server
"""

import socket
import pickle
import cv2
import numpy as np
import pyautogui

# ============ CHANGE THIS TO YOUR SERVER IP ============
SERVER_IP = "192.168.1.100"
SERVER_PORT = 5555
# =======================================================

def start_client():
    print("=" * 50)
    print("  SCREEN SHARE CLIENT")
    print("=" * 50)
    print(f"  Connecting to: {SERVER_IP}:{SERVER_PORT}")
    
    # Connect to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((SERVER_IP, SERVER_PORT))
        print("  Connected! Sharing screen...")
        print("=" * 50)
        
        while True:
            # Capture screen
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Compress as JPEG
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
            
            # Serialize
            data = pickle.dumps(buffer)
            
            # Send size header + data
            size = len(data)
            client.sendall(f"{size:<16}".encode())
            client.sendall(data)
            
    except Exception as e:
        print(f"  Error: {e}")
    
    finally:
        client.close()
        print("  Disconnected.")

if __name__ == "__main__":
    start_client()
