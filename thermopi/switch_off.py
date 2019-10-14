"""Turn off the thermostat."""

import logging

from thermopi import SetThermostat

LOGGER = logging.getLogger(__name__)


class SwitchOff(SetThermostat):
    """Turn off the thermostat."""

    def __init__(self, device, remote_device):
        """

        Parameters
        ----------
        device : XBeeDevice
            Local XBee device.
        remote_device : RemoteXBeeDevice
            Remote XBee device.
        """

        super().__init__(device, remote_device)

    def off(self, attempts=10):
        """Turn off the thermostat.

        Parameters
        ----------
        attempts : int
            Number of times to try to get the response from the thermostat.

        Raises
        -------
        FailedToGetState
            Failure to get the remote thermostat state.
        FailedToUpdateState
            Failed to update the thermostat.
        """

        self.set_state(0, False, False, False, attempts=attempts)
