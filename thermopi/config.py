"""Handle the loading of configuration files."""

import yaml


def load_config(config_file='/etc/thermopi.yaml'):
    """Load the configuration file.

    Parameters
    ----------
    config_file : str
        Path to the configuration file to load.

    Returns
    -------
    dict
        Dict containing the configuration file.
    """

    with open(config_file) as in_file:
        return yaml.load(in_file)
