"""
Models: VL53L1X and VL53L4CD
library: https://qwiic-vl53l1x-py.readthedocs.io/en/latest/index.html
"""
import qwiic_vl53l1x
import time

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