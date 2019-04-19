#!/usr/bin/env python3

from time import sleep

from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import TimeoutException

PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

REMOTE_STATE_REQUEST = bytearray([0x01])
SEND_STATE = bytearray([0x03])
REMOTE_NODE_ID = "Thermostat"

crc_table = [
  247, 250,  54, 124, 174,  56,  24,  25,  76, 240,  58,  22,  88,
  134,  30,  79, 114,  93, 154,  41, 238,  78, 102, 185, 153,   4,
  203, 252, 113,  10, 237,  92,   3,  70, 196,  32,  55, 140, 229,
  244, 242, 116, 106, 209, 204,  77, 144,  15, 253, 217, 164, 246,
  248, 216,  12,  49, 125, 226,  53, 207,  84, 239,  17,  62, 156,
  96,   7, 117, 233, 162, 111, 225, 130,  97, 219, 135, 227,  67,
  45, 141,  83, 243,   8, 118, 129,  59,  43, 188, 180,  86, 231,
  71, 206, 136, 184,  82,  50, 155, 210, 181,  95, 100,  90, 189,
  178,  35,  28, 126, 202, 171, 133, 224,  87, 165, 214, 168, 131,
  98, 128, 173, 249,  42, 255, 177, 119, 221, 208, 120, 132, 222,
  36, 193,  44,  85,  39, 183, 199, 123,  74,  73,  60, 159, 151,
  105,  57,  27, 170,  18,  89, 107,  23,  21, 145,  91, 201, 176,
  19, 192, 190, 115, 112, 230,  94, 245,  72,  75,  38, 152,  61,
  198,  46, 149,  63,  99, 127, 179, 215, 232,   6, 191,  66, 138,
  9,  80, 143,   5,  31,  81, 212,  14,  11, 146,  34, 150, 167,
  254,  69, 213, 142, 169, 235, 251, 122, 148, 163, 157, 137,  37,
  47,  65, 175, 110, 220, 158, 223,  13, 195,   1, 101,  20, 200,
  218, 234,  40, 228, 166, 205, 147, 194, 161, 211,  68,   0,  16,
  236, 109, 241,  64, 104,  51,  33, 182,   2, 121, 172,  48, 186,
  103, 108,  52, 197,  26, 187, 160,  29, 139
]

def crc_calc(data):
    # Calculate a CRC-8 of the object passed
    #
    # Source: https://www.maximintegrated.com/en/app-notes/index.mvp/id/27

    crc = 0x0;

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
            print('Sending request for current state')

            device.send_data(remote_device, data_to_send)

            print("Successfully sent")

            xbee_message = device.read_data(10) # Seconds

            # Verify CRC
            if crc_calc(xbee_message.data[2:]) != xbee_message.data[1]:
                print('CRC does not match! Try again...')
                raise TimeoutException # Lazy so using this for now
            else:
                print('CRC match')

            return xbee_message, None
        except TimeoutException:
            print("Timed out, try again")
            attempt += 1
            sleep(7)
    return True, 'Failed to get remote state'

def send_state(device, remote_device, data_to_send):
    """
    Send new state to remote
    """
    attempt = 0
    while attempt < 10:
        try:
            print("Sending data to %s >> %s..." % (remote_device.get_64bit_addr(), data_to_send))
            device.send_data(remote_device, data_to_send)

            print("Successfully sent")

            return None, None
        except Exception:
            print("Exception while trying to send state, trying again")
            attempt += 1
            sleep(7)
    return None, "Failed to send state to remote"


def main():
    print(" +--------------------------------------+")
    print(" | XBee send update to thermostat       |")
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

        # Send request for state
        xbee_message, err = get_remote_state(device, remote_device, REMOTE_STATE_REQUEST)
        if err:
            print(err)
            exit(1)
        data = xbee_message.data[1:]

        temp_setting = data[2]

        heat = cool = fan_mode = 0
        settings_to_send = bytearray([temp_setting, heat, cool, fan_mode])

        crc = bytearray([crc_calc(settings_to_send)])

        print('DATA_TYPE', SEND_STATE)
        print('crc_calc', crc_calc(settings_to_send))
        print('crc', crc[0])
        print('settings_to_send', settings_to_send)

        data_to_send = SEND_STATE + crc + settings_to_send

        send_state(device, remote_device, data_to_send)

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
