"""XBee access fo the thermostat."""

import logging
from time import sleep

from digi.xbee.exception import TimeoutException

from thermopi.crc import crc_calc
from thermopi.exceptions import CrcVerificationFailure, SendFailure, FailedToGetState

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

        self.data_type_get_remote_state = bytearray([0x01])  # Get remote state data type
        self.data_type_send_state = bytearray([0x03])  # Send state date type
        self.data_type_send_temperature = bytearray([0x10])  # Send temperature

    @staticmethod
    def gen_thermostat_msg(temp, heat, cool, fan):
        """

        Parameters
        ----------
        temp : int
            Temperature setting.
        heat : bool
            Heat on or off.
        cool : bool
            Cool on or off.
        fan : bool
            Fan on or off.

        Returns
        -------
        bytearray
            Contains the thermostat data converted to a byte array.
        """

        return bytearray([temp, heat, cool, fan])

    def get_remote_state(self, attempts=10, retry_sleep=7):
        """Get the remote stat from the thermostat.

        Parameters
        ----------
        attempts : int
            Number of times to try to get the response from the thermostat.
        retry_sleep : int
            How many seconds to wait between tries.

        Returns
        -------
        XBeeMessage
            The returned message the thermostat sent back.

        Raises
        ------
        CrcVerificationFailure
            The returned CRC is invalid.
        RetryException
            Multiple times have failed.
        """

        xbee_message = None

        for _ in range(attempts):
            LOGGER.info('Sending request for current state')
            self.device.send_data(self.remote_device, self.data_type_get_remote_state)
            LOGGER.info('Successfully sent')

            try:
                xbee_message = self.device.read_data(10)  # Seconds
            except TimeoutException:
                LOGGER.warning('Timed out')
                sleep(retry_sleep)
                continue

            if crc_calc(xbee_message.data[2:]) != xbee_message.data[1]:
                LOGGER.error('CRC does not match! Try again...')
                raise CrcVerificationFailure

            LOGGER.info('CRC match')
            break

        if xbee_message is None:
            raise FailedToGetState

        return xbee_message

    def send_state(self, data_to_send: bytearray, attempts: int = 10, retry_sleep: int = 7) -> object:
        """Send a new state config.yaml to the thermostat.

        Parameters
        ----------
        data_to_send
            Data to send to the remote device.
        attempts : int
            Number of times to try to send the data.
        retry_sleep : int
            How many seconds to wait between tries.

        Returns
        -------
        XBeePacket
            The response.

        Raises
        ------
        SendFailure
            If there is a failure to send the data.
        """

        crc = crc_calc(data_to_send)

        settings_to_send = self.data_type_send_state + bytes(crc) + data_to_send

        result = self.send(settings_to_send, attempts, retry_sleep)

        return result

    def send_temperature(self, temperature: int, sensor_id: int, attempts: int,
                         retry_sleep: int):
        """Send a temperature to the thermostat.

        Parameters
        ----------
        temperature : int
            Temperature data read from the temperature probe.
        sensor_id : int
            Sensor ID.
        attempts : int
            Number of times to try to send the data.
        retry_sleep : int
            How many seconds to wait between tries.

        Returns
        -------
        XBeePacket
            The response.

        Raises
        ------
        SendFailure
            If there is a failure to send the data.
        """

        temp_data = bytearray([temperature, sensor_id])

        temperature_to_send = self.data_type_send_temperature + crc_calc(temp_data) + temp_data

        result = self.send(temperature_to_send, attempts, retry_sleep)

        return result

    def send(self, data, attempts, retry_sleep):
        """

        Parameters
        ----------
        data : bytearray
            Data to send.
        attempts : int
            Number of times to try to send the data.
        retry_sleep : int
            How many seconds to wait between tries.

        Returns
        -------
        XBeePacket
            The response.

        Raises
        ------
        SendFailure
            If there is a failure to send the data.
        """

        result = None

        for _ in range(attempts):
            LOGGER.info('Sending data to {} -> {}...'.format(self.remote_device.get_64bit_addr(), data))
            try:
                result = self.device.send_data(self.remote_device, data)
                break
            except Exception as exception:
                LOGGER.error(exception)
                sleep(retry_sleep)

        if result is None:
            raise SendFailure

        return result
