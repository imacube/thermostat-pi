#!/usr/bin/env python3

from time import sleep

from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import TimeoutException

PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

DATA_TO_SEND = bytearray([0x01])
REMOTE_NODE_ID = "Thermostat"

crc_table = [
    247, 250, 54, 124, 174, 56, 24, 25, 76, 240, 58, 22, 88,
    134, 30, 79, 114, 93, 154, 41, 238, 78, 102, 185, 153, 4,
    203, 252, 113, 10, 237, 92, 3, 70, 196, 32, 55, 140, 229,
    244, 242, 116, 106, 209, 204, 77, 144, 15, 253, 217, 164, 246,
    248, 216, 12, 49, 125, 226, 53, 207, 84, 239, 17, 62, 156,
    96, 7, 117, 233, 162, 111, 225, 130, 97, 219, 135, 227, 67,
    45, 141, 83, 243, 8, 118, 129, 59, 43, 188, 180, 86, 231,
    71, 206, 136, 184, 82, 50, 155, 210, 181, 95, 100, 90, 189,
    178, 35, 28, 126, 202, 171, 133, 224, 87, 165, 214, 168, 131,
    98, 128, 173, 249, 42, 255, 177, 119, 221, 208, 120, 132, 222,
    36, 193, 44, 85, 39, 183, 199, 123, 74, 73, 60, 159, 151,
    105, 57, 27, 170, 18, 89, 107, 23, 21, 145, 91, 201, 176,
    19, 192, 190, 115, 112, 230, 94, 245, 72, 75, 38, 152, 61,
    198, 46, 149, 63, 99, 127, 179, 215, 232, 6, 191, 66, 138,
    9, 80, 143, 5, 31, 81, 212, 14, 11, 146, 34, 150, 167,
    254, 69, 213, 142, 169, 235, 251, 122, 148, 163, 157, 137, 37,
    47, 65, 175, 110, 220, 158, 223, 13, 195, 1, 101, 20, 200,
    218, 234, 40, 228, 166, 205, 147, 194, 161, 211, 68, 0, 16,
    236, 109, 241, 64, 104, 51, 33, 182, 2, 121, 172, 48, 186,
    103, 108, 52, 197, 26, 187, 160, 29, 139
]


def crc_calc(data):
    # Calculate a CRC-8 of the object passed
    #
    # Source: https://www.maximintegrated.com/en/app-notes/index.mvp/id/27

    crc = 0x0

    for d in data:
        crc = crc_table[crc ^ d]

    return crc


def get_remote_state(device, remote_device, data_to_send):
    """
    Get remote state
    """
    attempt = 0
    while attempt < 10:
        try:
            print("Sending data to %s >> %s..." % (remote_device.get_64bit_addr(), DATA_TO_SEND))

            device.send_data(remote_device, data_to_send)

            print("Success")

            xbee_message = device.read_data(10)  # Seconds
            return xbee_message
        except TimeoutException:
            print("Timed out, try again")
            attempt += 1
            sleep(7)


def main():
    print(" +--------------------------------------+")
    print(" | XBee send request for current state  |")
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

        xbee_message = get_remote_state(device, remote_device, DATA_TO_SEND)
        data = xbee_message.data[2:]

        """
        Struct used by the thermostat Arduino code:
        struct thermostatStruct {
            uint8_t _temp; // Current temperature
            uint8_t _temp_setting; // Temperature setting
            uint8_t _heat; // On or Off?
            uint8_t _heat_relay; // On or Off?
            uint8_t _cool; // On or Off?
            uint8_t _cool_relay; // On or Off?
            uint8_t _fan_mode; // Auto or On?
            uint8_t _fan_relay; // On or Off?
            unsigned long _run_stop; // When the system turned off, in milliseconds
            unsigned long _run_start; // When the system turned on, in milliseconds
          } thermostat_struct;
        """

        # print('data len', len(data))
        # print('start', data[8:12].hex())
        # print('start', data[12:16].hex())
        # print(data)
        print('Temperature', data[0])
        print('Temperature setting', data[1])
        print('Setting heat', False if data[2] == 0 else True)
        print('Setting heat relay', False if data[3] == 0 else True)
        print('Setting cool', False if data[4] == 0 else True)
        print('Setting cool relay', False if data[5] == 0 else True)
        print('Setting fan', False if data[6] == 0 else True)
        print('Setting fan relay', False if data[7] == 0 else True)
        print('Run stop', int.from_bytes(data[8:12], byteorder='little'))
        print('Run start', int.from_bytes(data[12:16], byteorder='little'))

        print('crc data', hex(xbee_message.data[1]))
        print('crc_calc', hex(crc_calc(xbee_message.data[2:])))

        if crc_calc(xbee_message.data[2:]) != xbee_message.data[1]:
            print('CRC does not match!')
        else:
            print('CRC match!')
    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
