"""Tests for Thermostat class which talks to the thermostat via the XBee radios."""

from unittest.mock import patch, MagicMock

from thermostat.thermostat import Thermostat


@patch('digi.xbee.devices.XBeeDevice')
@patch('digi.xbee.devices.RemoteXBeeDevice')
@patch('thermostat.thermostat.crc_calc')
class TestGetRemoteState:
    """Test methods in the Thermostat class."""

    def test_get_remote_state(self, mock_crc_calc, mock_remote, mock_device):
        """Test the get_remote_state method."""

        data_to_send = bytearray([0x01, 0x02, 0x03, 0x04])

        xbee_message = MagicMock()
        xbee_message.data = data_to_send
        mock_device.read_data.return_value = xbee_message
        mock_crc_calc.return_value = data_to_send[1]

        thermostat = Thermostat(mock_device, mock_remote)
        result = thermostat.get_remote_state(data_to_send, attempts=1, retry_sleep=0)

        assert result == xbee_message

        mock_device.send_data.assert_called_with(mock_remote, data_to_send)
        mock_device.read_data.assert_called_with(10)
        mock_crc_calc.assert_called_with(xbee_message.data[2:])
