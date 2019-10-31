#!/usr/bin/env python3

"""Read and send a temperature to the thermostat."""

from digi.xbee.devices import XBeeDevice

from thermopi import Thermostat

PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600
REMOTE_NODE_ID = "Thermostat"


def main():
    print(" +--------------------------------------+")
    print(" | XBee send temperature to thermostat  |")
    print(" +--------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        # Obtain the remote XBee device from the XBee network.
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        thermostat = Thermostat(device, remote_device)

        temp_identifier = bytearray([0x10])
        temp_data = bytearray([68, 0x10])

        result = thermostat.send_temperature(temp_identifier, temp_data)

        print('result: ', result)

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
