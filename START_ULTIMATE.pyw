import subprocess
import sys
import os

try:
    # Use tkinter to prompt for an IP since this file runs with pythonw (no console)
    import tkinter as tk
    from tkinter import simpledialog, messagebox

    root = tk.Tk()
    root.withdraw()

    default_ip = os.getenv("LAST_IP", "127.0.0.1")
    ip = simpledialog.askstring("Enter IP", "Enter the server IP for testers:", initialvalue=default_ip)
    if ip:
        # Save the IP to LAST_IP.txt so testers/clients can reuse it easily
        try:
            with open(os.path.join(os.path.dirname(__file__), "LAST_IP.txt"), "w", encoding="utf-8") as f:
                f.write(ip.strip())
        except Exception:
            pass
        try:
            messagebox.showinfo("Saved", f"Saved IP to LAST_IP.txt: {ip}")
        except Exception:
            pass
    root.destroy()
except Exception:
    # If tkinter isn't available or dialog fails, continue silently
    ip = None

venv_python = r"D:/SLIIT/Vs Code/remotess/.venv/Scripts/pythonw.exe"
server_script = os.path.join(os.path.dirname(__file__), "server_professional.py")

subprocess.Popen([venv_python, server_script],
                 creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
