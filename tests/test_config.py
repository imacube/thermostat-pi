"""Test the config.yaml module."""
import pytest

from thermopi.config import load_config


class TestLoadConfig:
    """Test the load_config method."""

    def test_success(self):
        """Test a successful loading of the configuration file."""

        expected_result = {'remote_xbee': 'thermostat'}

        try:
            result = load_config('tests/config.yaml')
        except FileNotFoundError:
            result = load_config('config.yaml')

        assert result == expected_result

    def test_file_not_found(self):
        """Test for a missing configuration file."""

        with pytest.raises(FileNotFoundError):
            load_config('nothing_to_see_here.yaml')
