import socket
import json
import struct
import threading
from message_types import MessageType

class TCPCommandServer:
    """Handterer TCP kommandoar frå PC"""
    
    def __init__(self, rvr_controller, port=8080):
        self.rvr = rvr_controller
        self.port = port
        self.running = False
        self.client_ip = None
        self.client_socket = None
    
    def start(self):
        """Start TCP server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(5)
        
        self.running = True
        print(f"TCP server lyttar på port {self.port}")
        
        # Accept connections
        while self.running:
            client_socket, address = self.server_socket.accept()
            print(f"Klient tilkopla: {address}")
            self.client_ip = address[0]
            
            # Handle in thread
            thread = threading.Thread(
                target=self._handle_client,
                args=(client_socket, address)
            )
            thread.start()
    
    def stop(self):
        """Stopp server"""
        self.running = False
        if hasattr(self, 'server_socket'):
            self.server_socket.close()
    
    def _read_u32(self, sock):
        """Les uint32"""
        data = sock.recv(4)
        if len(data) < 4:
            raise ConnectionError("Connection closed")
        return struct.unpack('>I', data)[0]
    
    def _receive_typed_frame(self, sock):
        """Motta typed frame"""
        size = self._read_u32(sock)
        if size == 0:
            return None, None
        
        data = bytearray()
        while len(data) < size:
            chunk = sock.recv(size - len(data))
            if not chunk:
                raise ConnectionError()
            data.extend(chunk)
        
        msg_type = data[0]
        payload = data[1:] if len(data) > 1 else bytearray()
        return msg_type, payload
    
    def _handle_client(self, sock, address):
        """Handter klient"""
        self.client_socket = sock
        try:
            while self.running:
                msg_type, payload = self._receive_typed_frame(sock)
                
                if msg_type is None:
                    break
                
                if msg_type == MessageType.CONTROL_COMMAND:
                    self._handle_control(payload)
                
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            self.rvr.stop()
            self.client_socket = None
            sock.close()
    
    def _handle_control(self, payload):
        """Handter kontroll-kommando frå C++"""
        data = json.loads(payload.decode('utf-8'))
        
        # Handter drive-kommandoar
        if 'left_stick_x' in data and 'left_stick_y' in data:
            x = float(data.get('left_stick_x', 0.0))
            y = float(data.get('left_stick_y', 0.0))
            self.rvr.drive(x, y)
        
        # Handter LED-kommandoar
        if 'r' in data and 'g' in data and 'b' in data:
            r = int(data.get('r', 0))
            g = int(data.get('g', 0))
            b = int(data.get('b', 0))
            self.rvr.set_leds(r, g, b)
        
        # Handter stopp-kommando
        if data.get('stop', False):
            self.rvr.stop()
    
    def _write_u32(self, sock, value):
        """Skriv uint32 i big-endian format"""
        buffer = struct.pack('>I', value)
        sock.send(buffer)
    
    def _send_typed_frame(self, sock, msg_type, payload):
        """Send typed frame til C++"""
        message = bytearray()
        message.append(msg_type)
        message.extend(payload)
        
        self._write_u32(sock, len(message))
        sock.send(message)
    
    def send_front_sensor_data(self, distance_mm):
        """Send front sensor data til C++"""
        if not self.client_socket:
            return
        
        try:
            data = {
                'distance': distance_mm,
                'sensor': 'front'
            }
            payload = json.dumps(data).encode('utf-8')
            self._send_typed_frame(self.client_socket, 
                                 MessageType.FRONT_SENSOR_DATA, 
                                 payload)
        except Exception as e:
            print(f"Error sending front sensor data: {e}")
    
    def send_rear_sensor_data(self, distance_mm):
        """Send rear sensor data til C++"""
        if not self.client_socket:
            return
        
        try:
            data = {
                'distance': distance_mm,
                'sensor': 'rear'
            }
            payload = json.dumps(data).encode('utf-8')
            self._send_typed_frame(self.client_socket, 
                                 MessageType.REAR_SENSOR_DATA, 
                                 payload)
        except Exception as e:
            print(f"Error sending rear sensor data: {e}")
