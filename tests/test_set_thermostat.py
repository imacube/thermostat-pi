"""Test the SetThermostat code."""

from unittest.mock import MagicMock, patch

import pytest

from thermopi import SetThermostat
from thermopi.exceptions import FailedToGetState, FailedToUpdateState


@pytest.fixture
def set_thermostat_objects():
    """Create mocks for XBee objects and build SetThermostat object with them.

    Returns
    -------
    tuple
        SetThermostat, mock_device, mock_remote_device
    """
    mock_device = MagicMock()
    mock_remote_device = MagicMock()

    mock_device_open = MagicMock()
    mock_device_open.is_open.return_value = True

    return SetThermostat(device=mock_device, remote_device=mock_remote_device), mock_device, mock_remote_device


@patch('thermopi.thermostat.Thermostat.get_remote_state')
@patch('thermopi.thermostat.Thermostat.send_state')
class TestSetThermostat:
    """Test the SetThermostat method code."""

    @pytest.mark.parametrize(
        "remote_after", [
            ([75, True, False, True]),
            ([75, True, False, False]),
            ([75, True, False, False]),
            ([75, False, True, False]),
            ([75, False, True, False]),
            ([75, False, True, True]),
        ])
    def test_success(self, mock_send_state, mock_get_remote_state, set_thermostat_objects, remote_after):
        """Test sending the thermostat state."""

        set_thermostat, mock_device, mock_remote_device = set_thermostat_objects

        remote_after_array = bytearray([255, 255, 255]) + bytearray(remote_after)

        class XBeeMessage:
            def __init__(self, data):
                self.data = data

        mock_get_remote_state.side_effect = [
            XBeeMessage(remote_after_array)
        ]

        temp, heat, cool, fan = remote_after
        set_thermostat.set_state(temp, heat, cool, fan)

        mock_device.open.assert_called_with()
        mock_send_state.assert_called_once_with(bytearray(remote_after))
        mock_get_remote_state.assert_called_with()

    @pytest.mark.parametrize(
        "remote_before, remote_after", [
            ([75, True, False, True], [75, True, False, False]),
            ([75, True, False, False], [75, True, False, True]),
            ([75, True, False, False], [75, False, True, False]),
            ([75, False, True, False], [75, False, True, True]),
            ([75, False, True, True], [75, False, True, False]),
            ([75, False, True, True], [75, True, False, True]),
        ])
    def test_success_same_temp(self, mock_send_state, mock_get_remote_state, set_thermostat_objects, remote_before,
                               remote_after):
        """Test sending the thermostat state."""

        set_thermostat, mock_device, mock_remote_device = set_thermostat_objects

        remote_before_array = bytearray([255, 255, 255]) + bytearray(remote_before)
        remote_after_array = bytearray([255, 255, 255]) + bytearray(remote_after)

        class XBeeMessage:
            def __init__(self, data):
                self.data = data

        mock_get_remote_state.side_effect = [
            XBeeMessage(remote_before_array),
            XBeeMessage(remote_after_array),
        ]

        _, heat, cool, fan = remote_after
        set_thermostat.set_state(0, heat, cool, fan)

        mock_device.open.assert_called_with()
        mock_send_state.assert_called_once_with(bytearray(remote_after))
        mock_get_remote_state.assert_called_with()

    def test_get_remote_state_failure(self, _, mock_get_remote_state, set_thermostat_objects):
        """Test for a FailedToGetState exception."""

        set_thermostat = set_thermostat_objects[0]

        mock_get_remote_state.side_effect = FailedToGetState

        with pytest.raises(FailedToGetState):
            set_thermostat.set_state(75, False, False, False)

    def test_failed_to_update_state(selfself, mock_send_state, mock_get_remote_state, set_thermostat_objects):
        """Test for a FailedToUpdateState exception."""

        set_thermostat, mock_device, mock_remote_device = set_thermostat_objects

        remote_after_expected = [75, True, False, True]
        remote_after_actual = [75, True, False, False]

        remote_after_actual_array = bytearray([255, 255, 255]) + bytearray(remote_after_actual)

        class XBeeMessage:
            def __init__(self, data):
                self.data = data

        mock_get_remote_state.return_value = XBeeMessage(remote_after_actual_array)

        temp, heat, cool, fan = remote_after_expected

        with pytest.raises(FailedToUpdateState):
            set_thermostat.set_state(temp, heat, cool, fan, attempts=1)

        mock_device.open.assert_called_with()
        mock_get_remote_state.assert_called_with()
        mock_send_state.assert_called_once_with(bytearray(remote_after_expected))
