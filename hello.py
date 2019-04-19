#!/usr/bin/env python3

from digi.xbee.devices import XBeeDevice

device = XBeeDevice('/dev/ttyUSB0', 9600)

device.open()

device.send_data_broadcast('Hello XBee World!')

device.close()
