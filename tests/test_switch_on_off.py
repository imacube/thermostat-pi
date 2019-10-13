"""Test the TurnOff code."""

from unittest.mock import MagicMock, patch

import pytest

from thermopi.exceptions import FailedToGetState
from thermopi.switch_on_off import SwitchOnOff


@pytest.fixture
def turn_off_objects():
    """Create mocks for XBee objects and build SwitchOnOff object with them.

    Returns
    -------
    tuple
        SwitchOnOff, mock_device, mock_remote_device
    """
    mock_device = MagicMock()
    mock_remote_device = MagicMock()

    mock_device_open = MagicMock()
    mock_device_open.is_open.return_value = True

    return SwitchOnOff(device=mock_device, remote_device=mock_remote_device), mock_device, mock_remote_device


@patch('thermopi.thermostat.Thermostat.get_remote_state')
@patch('thermopi.thermostat.Thermostat.send_state')
class TestTurnOff:
    """Test the TurnOff method code."""

    def test_success_off(self, mock_send_state, mock_get_remote_state, turn_off_objects):
        """Turn off the thermostat"""

        switch_on_off, mock_device, mock_remote_device = turn_off_objects

        remote_state_before_off = bytearray([255, 255, 255, 75, 0, 1, 1])
        remote_state_after_off = bytearray([255, 255, 255, 75, 0, 0, 0])

        class XBeeMessage:
            def __init__(self, data):
                self.data = data

        mock_get_remote_state.side_effect = [
            XBeeMessage(remote_state_before_off),
            XBeeMessage(remote_state_after_off)
        ]

        switch_on_off.off()

        mock_device.open.assert_called_with()
        mock_get_remote_state.assert_called_with()
        mock_send_state.assert_called_once_with(remote_state_after_off[3:])

    def test_get_remote_state_failure(self, _, mock_get_remote_state, turn_off_objects):
        """Test for a FailedToGetState exception."""

        switch_on_off, mock_device, mock_remote_device = turn_off_objects

        mock_get_remote_state.side_effect = FailedToGetState

        with pytest.raises(FailedToGetState):
            switch_on_off.off()
