import time


class ReadTemp:
    """Read temperature from temperature sensor."""

    def __init__(self, device_file):
        """

        Parameters
        ----------
        device_file : str
            Path to the file representing the temperature sensor.
        """

        self.device_file = device_file

    def read_temp_raw(self):
        """Read the lines from the file representing the temperature sensor.

        Returns
        -------
        list
            Return list of lines read from the file representing the temperature sensor.
        """

        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines


    def read_temp(self):
        """Get the temperature from the sensor.

        Returns
        -------
        tuple
            temperature in C, temperature in F
        """

        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f
