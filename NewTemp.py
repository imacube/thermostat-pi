#!/usr/bin/env python3

"""Read and send a temperature to the thermostat."""
import glob
import time

from digi.xbee.devices import XBeeDevice

from thermopi import Thermostat

PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600
REMOTE_NODE_ID = "Thermostat"

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


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

        _, temp_f = read_temp()

        temp_f = int(temp_f)

        print('Temp: {}'.format(temp_f))

        result = thermostat.send_temperature(temp_f, 0x10)

        print('result: ', result)

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
