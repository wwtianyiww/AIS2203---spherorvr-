"""
GPS module XA1110

library: https://github.com/sparkfun/qwiic_titan_gps_py/tree/main
"""
from time import sleep
from qwiicMUX import devices
import qwiic_titan_gps
import sys

class GPS:
    def __init__(self):
        self.gps = None
        self.initialized = False

    def initialize(self) -> bool:
        """Initialize GPS"""
        try:
            self.gps = qwiic_titan_gps.QwiicTitanGps()
            if self.gps.connected:
                self.gps.begin()
                self.initialized = True
                return True
            return False
        except:
            return False

    def read(self) -> dict:
        """
        Read GPS data

        Returns:
            Dict with lat/lon/time, or empty dict if no data
        """
        if not self.initialized:
            return {}

        try:
            if self.gps.get_nmea_data():
                return {
                    'lat': self.gps.gnss_messages.get('Latitude'),
                    'lon': self.gps.gnss_messages.get('Longitude'),
                    'time': self.gps.gnss_messages.get('Time')
                }
        except:
            pass

        return {}

