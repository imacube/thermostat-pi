"""Exceptions used by the thermostat module."""


class SendFailure(Exception):
    """Failed to send a message to the remote XBee."""


class CrcVerificationFailure(Exception):
    """CRC calculation didn't match expected value."""


class RetryException(Exception):
    """Multiple tries have failed."""
