"""
GPS module XA1110

library: https://github.com/sparkfun/qwiic_titan_gps_py/tree/main
"""
from time import sleep
import qwiic_titan_gps
import sys


def run_example():
    qwiicGPS = qwiic_titan_gps.QwiicTitanGps()

    if qwiicGPS.connected is False:
        print("Could not connect to to the SparkFun GPS Unit. Double check that\
              it's wired correctly.", file=sys.stderr)
        return

    qwiicGPS.begin()

    while True:
        try:
            if qwiicGPS.get_nmea_data() is True:
                print("Latitude: {}, Longitude: {}, Time: {}".format(
                    qwiicGPS.gnss_messages['Latitude'],
                    qwiicGPS.gnss_messages['Longitude'],
                    qwiicGPS.gnss_messages['Time'])) # Time will be UTC time as a list [hh, mm, ss]
        except:
            print("Error while retrieving GPS Values!")

        sleep(1)


if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending Basic Example.")
        sys.exit(0)