"""Tests for Thermostat class which talks to the thermostat via the XBee radios."""
from unittest.mock import patch

from thermostat.thermostat import Thermostat


class TestThermostat:
    """Test methods in the Thermostat class."""

    # @patch.object(devices, 'XBeeDevice', autospec=False)

    @patch('digi.xbee.devices.XBeeDevice')
    @patch('digi.xbee.devices.RemoteXBeeDevice')
    def test_get_remote_state(self, mock_device, mock_remote):
        """Test the get_remote_state method."""

        data_to_send = bytearray([0x01])

        thermostat = Thermostat(mock_device, mock_remote)

        thermostat.get_remote_state(data_to_send, attempts=0, retry_sleep=0)
