"""A set of helper functions."""

import ast
import configparser
import pathlib

import numpy as np

from uppyyl_observation_matcher.backend.helper import parse_config_value


def load_and_parse_config(config_file_path):
    """Load and parse the configuration file for the observation matcher.

    Args:
        config_file_path: The path of the config file.

    Returns:
        The parsed configuration data.
    """
    converters = {
        'dict': ast.literal_eval,
        'path': pathlib.Path,
    }
    config_parser = configparser.ConfigParser(converters=converters)
    config_parser._interpolation = configparser.ExtendedInterpolation()

    config_parser.read(config_file_path)
    config = {}
    for key, val in config_parser["config"].items():
        config[key] = parse_config_value(val)

    return config


def calculate_min_max_avg_int(vals):
    """Calculates the minimum, maximum, and average value of a given list.

    Args:
        vals: The value list.

    Returns:
        The minimum, maximum, and average value.
    """
    val_min = int(np.around(np.amin(vals)))
    val_max = int(np.around(np.amax(vals)))
    val_avg = int(np.around(np.average(vals)))
    return val_min, val_max, val_avg


def calculate_min_max_avg_float(vals):
    """Calculates the minimum, maximum, and average value of a given list.

    Args:
        vals: The value list.

    Returns:
        The minimum, maximum, and average value.
    """
    val_min = float(np.amin(vals))
    val_max = float(np.amax(vals))
    val_avg = float(np.average(vals))
    return val_min, val_max, val_avg


def get_model_details(uppyyl_simulator, model_data):
    """Get the details (e.g., component counts) of a model.

    Args:
        uppyyl_simulator: The Uppaal simulator into which the model has been loaded.
        model_data: The input model data containing the path.

    Returns:
        The model details dict.
    """
    uppyyl_simulator.load_model(model_data["path"])
    model_details = uppyyl_simulator.get_system_details()
    return model_details
