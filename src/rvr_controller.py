import sys
import os
sys.path.append(os.path.expanduser('~/sphero-sdk-raspberrypi-python'))

from sphero_sdk import SpheroRvrObserver
import math

class RVRController:
    """Handterer all RVR hardware-kontroll"""
    
    def __init__(self):
        self.rvr = SpheroRvrObserver()
        
    def initialize(self):
        """Start RVR"""
        print("Initialiserer RVR...")
        self.rvr.wake()
        self.rvr.reset_yaw()
        print("RVR klar!")
    
    def drive(self, left_stick_x, left_stick_y):
        """Køyr RVR basert på joystick input"""
        if abs(left_stick_x) > 0.1 or abs(left_stick_y) > 0.1:
            heading = int(math.degrees(math.atan2(left_stick_x, -left_stick_y)) % 360)
            magnitude = min(math.sqrt(left_stick_x**2 + left_stick_y**2), 1.0)
            speed = int(magnitude * 127)
            
            self.rvr.drive_with_heading(speed=speed, heading=heading, flags=0)
        else:
            self.stop()
    
    def stop(self):
        """Stopp RVR"""
        self.rvr.drive_stop()
    
    def set_leds(self, r, g, b):
        """Set LED-farge"""
        from sphero_sdk import LedGroups
        self.rvr.set_all_leds(
            led_group=LedGroups.all_lights,
            led_brightness_values=[r, g, b] * 10
        )
    
    def get_sensors(self):
        """Hent sensor-data"""
        # TODO: Implement sensor reading
        return {}
    
    def shutdown(self):
        """Steng av RVR"""
        self.stop()
        self.rvr.close()
