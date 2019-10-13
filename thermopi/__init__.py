"""thermopi can query and send commands to the house thermostat."""

import logging

# noinspection SpellCheckingInspection
LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s %(lineno)d - %(message)s'

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(console_handler)

from thermopi.thermostat import Thermostat
