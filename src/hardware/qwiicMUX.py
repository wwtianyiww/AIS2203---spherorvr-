"""
library: https://github.com/sparkfun/qwiic_tca9548a_py/tree/main
"""
from typing import Optional, List
import qwiic_tca9548a
import qwiic_i2c
import time
import sys


def initialize(self) -> List[int]:
    """Initialize mux and verify channels are enabled"""
    try:
        self.mux = qwiic_tca9548a.QwiicTCA9548A()

        if not self.mux.connected:
            print("ERROR: Mux not connected", file=sys.stderr)
            self.connected = False
            return []

        self.connected = True
        self.i2c = qwiic_i2c.getI2CDriver()
        self.mux.disable_all()

        # Enable channels
        channels_to_enable = [1, 2]
        self.mux.enable_channels(channels_to_enable)

        # VERIFY each channel is actually enabled
        verified_channels = []
        for channel in channels_to_enable:
            if self.mux.is_channel_enabled(channel):
                verified_channels.append(channel)
                print(f"✓ Channel {channel} verified enabled")
            else:
                print(f"✗ Channel {channel} failed to enable!", file=sys.stderr)

        # Only store successfully verified channels
        self.connected_channels = verified_channels

        # Optional: also print with list_channels() for visual check
        self.mux.list_channels()

        # Check if all channels enabled successfully
        if len(verified_channels) == len(channels_to_enable):
            self.initialized = True
            print(f"SUCCESS: All {len(verified_channels)} channels enabled")
        else:
            self.initialized = False
            print(f"WARNING: Only {len(verified_channels)}/{len(channels_to_enable)} channels enabled")

        return self.connected_channels

    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        self.initialized = False
        self.connected = False
        return []



