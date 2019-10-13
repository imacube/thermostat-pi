"""Tests for Thermostat class which talks to the thermostat via the XBee radios."""

from unittest.mock import patch, MagicMock

import pytest
from digi.xbee.exception import TimeoutException

from thermopi.exceptions import SendFailure
from thermopi.thermostat import Thermostat


@patch('digi.xbee.devices.XBeeDevice')
@patch('digi.xbee.devices.RemoteXBeeDevice')
class TestSendState:
    """Test a successful call of the method."""

    data_to_send = bytearray([0x01, 0x02, 0x03, 0x04])

    def test_success(self, mock_remote, mock_device):
        """Test a successful call of the method."""

        send_result = MagicMock()
        send_result.data = True
        mock_device.is_open.return_value = False
        mock_device.send_data.return_value = send_result

        thermostat = Thermostat(mock_device, mock_remote)
        result = thermostat.send_state(self.data_to_send, attempts=1, retry_sleep=0)

        assert result == send_result

        mock_device.send_data.assert_called_with(mock_remote, bytearray(b'\x03\xc2\x01\x02\x03\x04'))

    def test_send_failure(self, mock_remote, mock_device):
        """Test for a SendFailure exception being raised."""

        mock_device.send_data.side_effect = TimeoutException

        thermostat = Thermostat(mock_device, mock_remote)

        with pytest.raises(SendFailure):
            thermostat.send_state(self.data_to_send, attempts=3, retry_sleep=0)
