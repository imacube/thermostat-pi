"""Set the thermostat state."""

import logging

from thermopi import Thermostat
from thermopi.exceptions import FailedToUpdateState

LOGGER = logging.getLogger(__name__)


class SetThermostat(Thermostat):
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

    def set_state(self, temp, heat, cool, fan, attempts=10):
        """Turn off the thermostat.

        Parameters
        ----------
        temp : int
            Temperature setting. Set to 0 to keep current temp.
        heat : bool
            Heat on or off.
        cool : bool
            Cool on or off.
        fan : bool
            Fan on or off.
        attempts : int
            Number of times to try to get the response from the thermostat.

        Raises
        -------
        FailedToGetState
            Failure to get the remote thermostat state.
        FailedToUpdateState
            Failed to update the thermostat.
        """

        success = False

        try:
            self.device.open()

            for _ in range(attempts):
                if temp == 0:
                    xbee_message = self.get_remote_state()
                    data = xbee_message.data[3:]
                    temp_setting = data[0]
                else:
                    temp_setting = temp

                settings_to_send = bytearray([temp_setting, heat, cool, fan])

                LOGGER.info('settings_to_send {}'.format(settings_to_send))
                result = self.send_state(settings_to_send)
                LOGGER.info(result)

                xbee_message = self.get_remote_state()
                data = xbee_message.data[3:]
                if settings_to_send == data:
                    success = True
                    break

                LOGGER.critical('Failed to set the thermostat!')

            if not success:
                raise FailedToUpdateState

        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
