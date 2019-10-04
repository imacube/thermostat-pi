"""Exceptions used by the thermostat module."""

def CrcVerificationFailure(Exception):
    """CRC calculation didn't match expected value."""

def RetryException(Exception):
    """Multiple tries have failed."""