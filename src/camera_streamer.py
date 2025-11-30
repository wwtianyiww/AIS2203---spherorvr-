import cv2
import socket
import threading
import time

class CameraStreamer:
    """Handterer UDP video streaming"""
    
    def __init__(self, target_ip, port=9999, quality=80):
        self.target_ip = target_ip
        self.port = port
        self.quality = quality
        self.running = False
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.camera = None
    
    def initialize(self):
        """Opne kamera"""
        print("Åpner kamera...")
        self.camera = cv2.VideoCapture(0)
        
        if not self.camera.isOpened():
            print("Warning: Kunne ikkje opne kamera")
            return False
        
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        print("Kamera klar!")
        return True
    
    def start(self):
        """Start streaming i bakgrunnen"""
        if not self.camera:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.thread.start()
        print(f"Streaming til {self.target_ip}:{self.port}")
    
    def stop(self):
        """Stopp streaming"""
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join(timeout=2.0)
        if self.camera:
            self.camera.release()
        self.sock.close()
    
    def _stream_loop(self):
        """Streaming loop"""
        while self.running:
            ret, frame = self.camera.read()
            if not ret:
                continue
            
            _, jpeg = cv2.imencode('.jpg', frame, 
                                   [cv2.IMWRITE_JPEG_QUALITY, self.quality])
            data = jpeg.tobytes()
            
            try:
                self.sock.sendto(data, (self.target_ip, self.port))
            except Exception as e:
                print(f"Streaming error: {e}")
            
            time.sleep(0.001)
