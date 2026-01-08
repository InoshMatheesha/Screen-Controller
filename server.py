"""
Simple Screen Share Server
- Receives screen images from client
- Displays in a window
"""

import socket
import pickle
import cv2
import numpy as np

def start_server():
    # Create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    server.listen(1)
    
    # Get my IP to display
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()
    
    print("=" * 50)
    print("  SCREEN SHARE SERVER")
    print("=" * 50)
    print(f"  Your IP: {my_ip}")
    print(f"  Port: 5555")
    print("=" * 50)
    print("  Waiting for connection...")
    print("=" * 50)
    
    # Wait for client to connect
    client_socket, address = server.accept()
    print(f"\n  Connected: {address[0]}")
    print("  Receiving screen... (Press Q to quit)")
    
    try:
        while True:
            # Receive size header (16 bytes)
            size_data = client_socket.recv(16)
            if not size_data:
                break
            
            # Get message size
            msg_size = int(size_data.decode().strip())
            
            # Receive image data
            data = b''
            while len(data) < msg_size:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data += packet
            
            if len(data) < msg_size:
                break
            
            # Decode image
            img_data = pickle.loads(data)
            frame = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
            
            # Resize to fit screen
            frame = cv2.resize(frame, (1280, 720))
            
            # Show image
            cv2.imshow('Screen Share - Press Q to quit', frame)
            
            # Press Q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"  Error: {e}")
    
    finally:
        client_socket.close()
        server.close()
        cv2.destroyAllWindows()
        print("\n  Server stopped.")

if __name__ == "__main__":
    start_server()
