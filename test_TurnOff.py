from TurnOff import crc_calc


def test_crc_calc():
    """Test TurnOff.crc_calc"""

    temp_setting = 1
    heat = 2
    cool = 3
    fan_mode = 4
    other_data = 5

    settings_to_send = bytearray([temp_setting, heat, cool, fan_mode, other_data])
    crc = bytearray([crc_calc(settings_to_send)])

    assert crc_calc(crc) == 198
