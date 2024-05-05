"""The configurations of the observations."""

import copy

from uppyyl_observation_matcher_experiments.backend.helper import load_and_parse_config
from uppyyl_observation_matcher_experiments.definitions import RES_DIR

########################################################################################################################
# Main configuration file #
########################################################################################################################
main_config_file_path = RES_DIR.joinpath(f'config.ini')

########################################################################################################################
# Base configurations #
########################################################################################################################
base_observation_config = load_and_parse_config(config_file_path=main_config_file_path)
base_observation_config.update({
    "allow_variable_observations": True,
    "observed_variables": [],  # Format: ["var1", "var2", ...], use None or [] to observe all model variables

    "allow_partial_observations": False,

    "default_deviation_bounds": (0, 0),
    "allowed_deviations_in_observations": {},  # Format: {"var1": [a, b], "var2": [c, d], ...}

    "allow_location_observations": False,
    "observed_processes_for_locations": [],  # Format: ["proc1", "proc2", ...], use None or [] to observe all locations

    "time_shift_bounds": (0, 0),

    "allow_committed_observations": False,

    "concrete_transition_times": "random",  # min, max, random
    "force_keep_first_observation": False,
    "force_keep_last_observation": False,

    "step_count": 1,
    "observation_count_bounds": (1, 1),  # Min and max bound for numbers of data points in obs (must be <= step_count)
})

########################################################################################################################
# Matcher model configurations #
########################################################################################################################
all_observation_configs = {}

# Base observation configuration
all_observation_configs["B"] = copy.deepcopy(base_observation_config)

# Partial data observation configuration
all_observation_configs["P"] = copy.deepcopy(base_observation_config)
all_observation_configs["P"].update({
    "allow_partial_observations": True
})

# Deviating data observation configuration
all_observation_configs["D"] = copy.deepcopy(base_observation_config)
all_observation_configs["D"].update({
    "default_deviation_bounds": (1, 5)
})

# Location data observation configuration
all_observation_configs["L"] = copy.deepcopy(base_observation_config)
all_observation_configs["L"].update({
    # "allow_variable_observations": False,
    "allow_location_observations": True,
})

# Time-shifted data observation configuration
all_observation_configs["S"] = copy.deepcopy(base_observation_config)
all_observation_configs["S"].update({
    "time_shift_bounds": (1, 10),
})

# Committed location data observation configuration
all_observation_configs["C"] = copy.deepcopy(base_observation_config)
all_observation_configs["C"].update({
    "allow_committed_observations": True,
})

# All advanced features observation configuration
all_observation_configs["All"] = copy.deepcopy(base_observation_config)
all_observation_configs["All"].update({
    "allow_partial_observations": True,
    "default_deviation_bounds": (1, 5),
    "allow_location_observations": True,
    "time_shift_bounds": (1, 10),
    "allow_committed_observations": True,
})
