"""
library: https://github.com/sparkfun/qwiic_tca9548a_py/tree/main
"""

import qwiic_tca9548a
import qwiic_i2c
import time
import sys


def runExample():
    print("\nSparkFun TCA9548A 8-Channel Mux Example 1\n")

    myTca = qwiic_tca9548a.QwiicTCA9548A()

    if myTca.connected == False:
        print("The Qwiic TCA9548A 8-Channel Mux device isn't connected to the system. Please check your connection", \
              file=sys.stderr)
        return

    # We will use this object to see what devices are connected to the master after configuring the MUX
    i2c = qwiic_i2c.getI2CDriver()

    while True:
        # By enabling channels 0 and 1, our Master device can speak to a device connected to port 0 or 1of the MUX
        print("Enabling channels 0 and 1")
        myTca.disable_all()
        myTca.enable_channels([0, 1])
        myTca.list_channels()

        # Find any i2c devices connected to the master, we should see the addresses of any devices we have connected to port 0 or 1 here,
        # but not any devices connected to other ports.
        print("Checking for i2c devices on ports 0 and 1")
        devices = i2c.scan()
        print("Devices found: ", devices)
        time.sleep(2)

        # Enable channels 2 and 3, our Master device can now speak to a device connected to port 2 or 3 of the MUX
        print("Enabling channels 2 and 3")
        myTca.disable_all()
        myTca.enable_channels([2, 3])
        myTca.list_channels()

        # Find any i2c devices connected to the master, we should see the addresses of any devices we have connected to port 2 or 3 here,
        # but not any devices connected to other ports.
        print("Checking for i2c devices on ports 2 and 3")
        devices = i2c.scan()
        print("Devices found: ", devices)
        time.sleep(2)


if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)


