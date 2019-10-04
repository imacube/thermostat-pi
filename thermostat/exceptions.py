"""Exceptions used by the thermostat module."""


class CrcVerificationFailure(Exception):
    """CRC calculation didn't match expected value."""


class RetryException(Exception):
    """Multiple tries have failed."""
