"""XBee access fo the thermostat."""

import logging
from time import sleep

from digi.xbee.exception import TimeoutException

from thermostat.crc import crc_calc

LOGGER = logging.getLogger(__name__)


class Thermostat:
    """XBee access of the thermostat."""

    def __init__(self, device, remote_device):
        """

        Parameters
        ----------
        device : XBeeDevice
            Local XBee device.
        remote_device : RemoteXBeeDevice
            Remote XBee device.
        """

        self.device = device
        self.remote_device = remote_device

    def get_remote_state(self, data_to_send, attempts=10, retry_sleep=7):
        """Get the remote stat from the thermostat.

        Parameters
        ----------
        data_to_send : bytearray
            Payload to send to thermostat.
        attempts : int
            Number of times to try to get the response from the thermostat.
        retry_sleep : int
            How many seconds to wait between tries.

        Returns
        -------
        XBeeMessage
            The returned message the thermostat sent back.
        """

        attempt = 0
        while attempt < attempts:
            try:
                LOGGER.info('Sending request for current state')

                self.device.send_data(self.remote_device, data_to_send)

                LOGGER.info('Successfully sent')

                xbee_message = self.device.read_data(10)  # Seconds

                # Verify CRC
                if crc_calc(xbee_message.data[2:]) == xbee_message.data[1]:
                    LOGGER.info('CRC match')
                else:
                    LOGGER.error('CRC does not match! Try again...')
                    raise TimeoutException  # Lazy so using this for now

                return xbee_message, None
            except TimeoutException:
                LOGGER.warning('Timed out, try again')
                attempt += 1
                sleep(retry_sleep)

        return None, 'Failed to get remote state'
