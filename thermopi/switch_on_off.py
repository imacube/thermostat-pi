import logging

from thermopi import Thermostat

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

    def off(self, temp=0, attempts=10):
        """Turn off the thermostat.

        Parameters
        ----------
        temp : int
            0 for no change to the temperature, else the value set on the thermostat.
        attempts : int
            Number of times to try to get the response from the thermostat.

        Raises
        -------
        FailedToGetState
            Failure to get the remote thermostat state.
        FailedToUpdateState
            Failed to update the thermostat.
        """

        try:
            self.device.open()

            xbee_message = self.get_remote_state()

            data = xbee_message.data[1:]

            temp_setting = data[2]

            heat = cool = fan_mode = 0
            settings_to_send = bytearray([temp_setting, heat, cool, fan_mode])

            LOGGER.info('settings_to_send', settings_to_send)

            result = self.send_state(settings_to_send)
            LOGGER.info(result)

        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
