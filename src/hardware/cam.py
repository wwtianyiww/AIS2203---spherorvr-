
import socket
import threading
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import io


class UDPOutput(FileOutput):
     
    
    def __init__(self, udp_host: str, udp_port: int):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_host = udp_host
        self.udp_port = udp_port
        
    def outputframe(self, frame, keyframe=True, timestamp=None):
        
        # H.264 NAL units
        chunk_size = 60000
        for i in range(0, len(frame), chunk_size):
            chunk = frame[i:i+chunk_size]
            try:
                self.sock.sendto(chunk, (self.udp_host, self.udp_port))
            except Exception as e:
                print(f"UDP error: {e}")


class Camera:
    
    def __init__(self, udp_host: str, udp_port: int, 
                 resolution: tuple = (640, 480), framerate: int = 30):
        self.udp_host = udp_host
        self.udp_port = udp_port
        self.resolution = resolution
        self.framerate = framerate
        
        self.camera = None
        self.encoder = None
        self.output = None
        self.running = False
        
        print(f"Camera init - {resolution[0]}x{resolution[1]} @ {framerate}fps")
        print(f"UDP: {udp_host}:{udp_port}")
    
    def start(self):

        if self.running:
            return
        
        try:

            self.camera = Picamera2()
            
            # Configure for video
            video_config = self.camera.create_video_configuration(
                main={"size": self.resolution, "format": "RGB888"},
                controls={"FrameRate": self.framerate}
            )
            self.camera.configure(video_config)
            
            #H.264 encoder)
            self.encoder = H264Encoder(bitrate=1000000)  # 1 Mbps
            
            #UDP output
            self.output = UDPOutput(self.udp_host, self.udp_port)
            
            #encoding
            self.camera.start_recording(self.encoder, self.output)
            self.running = True
            
            print("Camera started")
            
        except Exception as e:
            print(f"Error: {e}")
            self.stop()
    
    def stop(self):
        if not self.running:
            return
        
        self.running = False
        
        if self.camera:
            if self.camera.started:
                self.camera.stop_recording()
            self.camera.close()
            self.camera = None
        
        if self.output and hasattr(self.output, 'sock'):
            self.output.sock.close()
        
        print("Camera stopped")
    
    def is_running(self):
        return self.running


# Test
if __name__ == "__main__":
    cam = Camera("192.168.1.100", 5000, (640, 480), 30)
    try:
        cam.start()
        print("Streaming... Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cam.stop()
