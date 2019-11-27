import pytest

from thermopi import Thermostat


class TestGenThermostatMsg:
    def test_temp(self):
        """Test temp setting."""

        thermostat = Thermostat(None, None)

        temp_setting = 75
        assert bytearray([75, 0, 0, 0]) == thermostat.gen_thermostat_msg(75, False, False, False)

    def test_heat(self):
        """Test heat setting."""

        thermostat = Thermostat(None, None)

        temp_setting = 75
        assert bytearray([75, 1, 0, 0]) == thermostat.gen_thermostat_msg(75, True, False, False)

    def test_cool(self):
        """Test cool setting."""

        thermostat = Thermostat(None, None)

        temp_setting = 75
        assert bytearray([75, 0, 1, 0]) == thermostat.gen_thermostat_msg(75, False, True, False)

    def test_fan(self):
        """Test fan setting."""

        thermostat = Thermostat(None, None)

        temp_setting = 75
        assert bytearray([75, 0, 0, 1]) == thermostat.gen_thermostat_msg(75, False, False, True)

    def test_heat_fan(self):
        """Test heat and fan setting."""

        thermostat = Thermostat(None, None)

        temp_setting = 75
        assert bytearray([75, 1, 0, 1]) == thermostat.gen_thermostat_msg(75, True, False, True)

    def test_cool_fan(self):
        """Test cool and fan setting."""

        thermostat = Thermostat(None, None)

        temp_setting = 75
        assert bytearray([75, 0, 1, 1]) == thermostat.gen_thermostat_msg(75, False, True, True)