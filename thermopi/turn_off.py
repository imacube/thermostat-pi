
def turn_off():
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