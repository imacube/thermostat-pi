"""Tests for Thermostat class which talks to the thermostat via the XBee radios."""

from unittest.mock import patch, MagicMock

import pytest
from digi.xbee.exception import TimeoutException

from thermostat.exceptions import RetryException
from thermostat.thermostat import Thermostat


@patch('digi.xbee.devices.XBeeDevice')
@patch('digi.xbee.devices.RemoteXBeeDevice')
@patch('thermostat.thermostat.crc_calc')
class TestGetRemoteState:
    """Test methods in the Thermostat class."""

    data_to_send = bytearray([0x01, 0x02, 0x03, 0x04])

    def test_success(self, mock_crc_calc, mock_remote, mock_device):
        """Test the get_remote_state method."""

        xbee_message = MagicMock()
        xbee_message.data = self.data_to_send
        mock_device.read_data.return_value = xbee_message
        mock_crc_calc.return_value = self.data_to_send[1]

        thermostat = Thermostat(mock_device, mock_remote)
        result = thermostat.get_remote_state(self.data_to_send, attempts=1, retry_sleep=0)

        assert result == xbee_message

        mock_device.send_data.assert_called_with(mock_remote, self.data_to_send)
        mock_device.read_data.assert_called_with(10)
        mock_crc_calc.assert_called_with(xbee_message.data[2:])

    def test_retry_exception(self, _, mock_remote, mock_device):
        """Test for a RetryException."""

        mock_device.read_data.side_effect = TimeoutException

        thermostat = Thermostat(mock_device, mock_remote)

        with pytest.raises(RetryException):
            thermostat.get_remote_state(self.data_to_send, attempts=3, retry_sleep=0)
