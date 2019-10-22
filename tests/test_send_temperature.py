"""Tests for Thermostat class which talks to the thermostat via the XBee radios."""

from unittest.mock import patch, MagicMock

import pytest
from digi.xbee.exception import TimeoutException

from thermopi.exceptions import FailedToGetState
from thermopi.thermostat import Thermostat


@patch('digi.xbee.devices.XBeeDevice')
@patch('digi.xbee.devices.RemoteXBeeDevice')
@patch('thermopi.thermostat.crc_calc')
class TestSendTemperature:
    """Test the send_temperature method."""

    temperature = 68
    sensor_id = 0x10

    def test_success(self, mock_crc_calc, mock_remote, mock_device):
        """Test a successful call of the method."""

        temp_data = bytearray([self.temperature, self.sensor_id])

        xbee_message = MagicMock()
        mock_device.read_data.return_value = xbee_message
        mock_crc_calc.return_value = temp_data

        thermostat = Thermostat(mock_device, mock_remote)
        thermostat.send_temperature(temp_identifier=0x10, temperature=self.temperature,
                                    sensor_id=self.sensor_id, attempts=1, retry_sleep=0)

        mock_device.send_data.assert_called_with(mock_remote, bytearray([0x10]) + temp_data + temp_data)
        mock_crc_calc.assert_called_with(temp_data)

    def test_retry_exception(self, _, mock_remote, mock_device):
        """Test for a RetryException exception being raised."""

        mock_device.read_data.side_effect = TimeoutException

        thermostat = Thermostat(mock_device, mock_remote)

        with pytest.raises(FailedToGetState):
            thermostat.get_remote_state(attempts=1, retry_sleep=0)
