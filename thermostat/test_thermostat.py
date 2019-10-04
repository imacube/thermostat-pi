"""Tests for Thermostat class which talks to the thermostat via the XBee radios."""

from unittest.mock import patch, MagicMock

import pytest
from digi.xbee.exception import TimeoutException

from thermostat.exceptions import RetryException, CrcVerificationFailure, SendFailure
from thermostat.thermostat import Thermostat


@patch('digi.xbee.devices.XBeeDevice')
@patch('digi.xbee.devices.RemoteXBeeDevice')
@patch('thermostat.thermostat.crc_calc')
class TestGetRemoteState:
    """Test the get_remote_state method."""

    data_to_send = bytearray([0x01, 0x02, 0x03, 0x04])

    def test_success(self, mock_crc_calc, mock_remote, mock_device):
        """Test a successful call of the method."""

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
        """Test for a RetryException exception being raised."""

        mock_device.read_data.side_effect = TimeoutException

        thermostat = Thermostat(mock_device, mock_remote)

        with pytest.raises(RetryException):
            thermostat.get_remote_state(self.data_to_send, attempts=3, retry_sleep=0)

    def test_crc_verification_failure(self, mock_crc_calc, mock_remote, mock_device):
        """Test for a CrcVerificationFailure exception being raised."""

        xbee_message = MagicMock()
        xbee_message.data = self.data_to_send
        mock_device.read_data.return_value = xbee_message
        mock_crc_calc.return_value = self.data_to_send[1:2]

        thermostat = Thermostat(mock_device, mock_remote)

        with pytest.raises(CrcVerificationFailure):
            thermostat.get_remote_state(self.data_to_send, attempts=1, retry_sleep=0)


@patch('digi.xbee.devices.XBeeDevice')
@patch('digi.xbee.devices.RemoteXBeeDevice')
class TestSendState:
    """Test a successful call of the method."""

    data_to_send = bytearray([0x01, 0x02, 0x03, 0x04])

    def test_success(self, mock_remote, mock_device):
        """Test a successful call of the method."""

        send_result = MagicMock()
        send_result.data = True
        mock_device.send_data.return_value = send_result

        thermostat = Thermostat(mock_device, mock_remote)
        result = thermostat.send_state(self.data_to_send, attempts=1, retry_sleep=0)

        assert result == send_result

        mock_device.send_data.assert_called_with(mock_remote, self.data_to_send)
        mock_device.send_data.assert_called_with(mock_remote, self.data_to_send)

    def test_send_failure(self, mock_remote, mock_device):
        """Test for a SendFailure exception being raised."""

        mock_device.send_data.side_effect = TimeoutException

        thermostat = Thermostat(mock_device, mock_remote)

        with pytest.raises(SendFailure):
            thermostat.send_state(self.data_to_send, attempts=3, retry_sleep=0)
