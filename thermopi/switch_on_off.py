import logging

from thermopi import Thermostat
from thermopi.exceptions import FailedToUpdateState

LOGGER = logging.getLogger(__name__)


class SwitchOnOff(Thermostat):
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

        success = False

        try:
            self.device.open()

            for _ in range(attempts):
                xbee_message = self.get_remote_state()
                data = xbee_message.data[3:]

                temp_setting = data[0]
                heat = cool = fan_mode = 0
                settings_to_send = self.gen_thermostat_msg(temp_setting, heat, cool, fan_mode)

                LOGGER.info('settings_to_send {}'.format(settings_to_send))
                result = self.send_state(settings_to_send)
                LOGGER.info(result)

                xbee_message = self.get_remote_state()
                data = xbee_message.data[3:]
                if settings_to_send == data:
                    success = True
                    break

                LOGGER.critical('Failed to turn off Thermostat!')

            if not success:
                raise FailedToUpdateState

        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
