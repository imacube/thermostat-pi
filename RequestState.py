from digi.xbee.devices import XBeeDevice

PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

DATA_TO_SEND = bytearray([0x01])
REMOTE_NODE_ID = "Thermostat"


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

        print("Sending data to %s >> %s..." % (remote_device.get_64bit_addr(), DATA_TO_SEND))

        device.send_data(remote_device, DATA_TO_SEND)

        print("Success")

        xbee_message = device.read_data(10) # Seconds
        print(xbee_message.data)

        for b in xbee_message.data:
            print(hex(b))

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
