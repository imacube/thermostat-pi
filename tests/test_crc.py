import pytest

from thermopi.crc import crc_calc


class TestCrc:
    def test_crc_success(self):
        """Test TurnOff.crc_calc"""

        temp_setting = 1
        heat = 2
        cool = 3
        fan_mode = 4
        other_data = 5

        settings_to_send = bytearray([temp_setting, heat, cool, fan_mode, other_data])
        crc = crc_calc(settings_to_send)
        crc = bytearray([crc])

        assert bytearray(b'\xa9') == crc

    def test_crc_failure(self):
        """Test for a crc_calc method failure."""

        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            crc_calc(3.3)
