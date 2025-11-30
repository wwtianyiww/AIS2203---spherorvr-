"""
Models: VL53L1X and VL53L4CD
library: https://qwiic-vl53l1x-py.readthedocs.io/en/latest/index.html
"""
import qwiic_vl53l1x
import time
from typing import Optional


class DistanceSensor:
    def __init__(self, name: str):
        """
        Initialize a distance sensor

        Args:
            name: Identifier for this sensor (e.g., "front", "back")
        """
        self.name = name
        self.sensor: Optional[qwiic_vl53l1x.QwiicVL53L1X] = None
        self.initialized = False
        self.last_distance: Optional[int] = None

    def initialize(self) -> bool:
        """
        Initialize the sensor hardware
        Returns:
            True if successful, False otherwise
        """
        try:
            self.sensor = qwiic_vl53l1x.QwiicVL53L1X()

            # sensor_init() returns None on success
            if self.sensor.sensor_init() is None:
                self.initialized = True
                print(f"✓ {self.name} sensor online")
                return True
            else:
                print(f"✗ {self.name} sensor failed to initialize")
                return False

        except Exception as e:
            print(f"✗ {self.name} sensor error: {e}")
            return False

    def read_distance(self) -> Optional[int]:
        """
        Read distance from sensor

        Returns:
            Distance in millimeters, or None if error
        """
        if not self.initialized or not self.sensor:
            return None

        try:
            self.sensor.start_ranging()
            time.sleep(0.005)
            distance = self.sensor.get_distance()
            time.sleep(0.005)
            self.sensor.stop_ranging()

            self.last_distance = distance
            return distance

        except Exception as e:
            print(f"Error reading {self.name}: {e}")
            return None

    def get_last_distance(self) -> Optional[int]:
        """Get the last successfully read distance"""
        return self.last_distance

    def cleanup(self):
        """Stop ranging"""
        if self.sensor and self.initialized:
            try:
                self.sensor.stop_ranging()
            except:
                pass

"""
# vurder å endre til map med key: "front", "back"
distanceSensorFront = qwiic_vl53l1x.QwiicVL53L1X()
distanceSensorBack = qwiic_vl53l1x.QwiicVL53L1X()
sensors = [distanceSensorFront, distanceSensorBack]

for s in sensors:
    if (s.sensor_init() == None):					 # Begin returns 0 on a good init
	print(f"{s} sensor online!\n")


while True:
    try:
        for s in sensors:
            s.stop_ranging()
            time.sleep(.005)
            distance = s.get_distance()	 # Get the result of the measurement from the sensor
            time.sleep(.005)
            s.stop_ranging()

    except Exception as e:
		print(e)
"""
