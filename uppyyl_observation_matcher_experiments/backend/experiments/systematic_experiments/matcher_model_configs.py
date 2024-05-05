"""The configurations of the matcher model."""

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
base_matcher_model_config = load_and_parse_config(config_file_path=main_config_file_path)
base_matcher_model_config.update({
    "support_partial_matching": False,
    "support_deviating_matching": False,
    "support_location_matching": False,
    "support_shifted_matching": False,
    "support_committed_matching": False,
    "allowed_deviations": {},
    "maximum_initial_delay": 0,
})

########################################################################################################################
# Matcher model configurations #
########################################################################################################################
all_matcher_model_configs = {}

# Raw matcher model configuration
all_matcher_model_configs["R"] = copy.deepcopy(base_matcher_model_config)

# Simplified base matcher model configuration
all_matcher_model_configs["B"] = copy.deepcopy(base_matcher_model_config)

# Simplified base matcher model (+ partial data) configuration
all_matcher_model_configs["B+P"] = copy.deepcopy(base_matcher_model_config)
all_matcher_model_configs["B+P"].update({
    "support_partial_matching": True
})

# Simplified base matcher model (+ deviation) configuration
all_matcher_model_configs["B+D"] = copy.deepcopy(base_matcher_model_config)
all_matcher_model_configs["B+D"].update({
    "support_deviating_matching": True
})

# Simplified base matcher model (+ location matching) configuration
all_matcher_model_configs["B+L"] = copy.deepcopy(base_matcher_model_config)
all_matcher_model_configs["B+L"].update({
    "support_location_matching": True
})

# Simplified base matcher model (+ time shifts) configuration
all_matcher_model_configs["B+S"] = copy.deepcopy(base_matcher_model_config)
all_matcher_model_configs["B+S"].update({
    "support_shifted_matching": True
})

# Simplified base matcher model (+ committed matching) configuration
all_matcher_model_configs["B+C"] = copy.deepcopy(base_matcher_model_config)
all_matcher_model_configs["B+C"].update({
    "support_committed_matching": True
})

# Simplified base matcher model (+ time shifts + committed matching) configuration
all_matcher_model_configs["B+S+C"] = copy.deepcopy(base_matcher_model_config)
all_matcher_model_configs["B+S+C"].update({
    "support_shifted_matching": True,
    "support_committed_matching": True
})

# Simplified base matcher model (+ all advanced features) configuration
all_matcher_model_configs["All"] = copy.deepcopy(base_matcher_model_config)
all_matcher_model_configs["All"].update({
    "support_partial_matching": True,
    "support_deviating_matching": True,
    "support_location_matching": True,
    "support_shifted_matching": True,
    "support_committed_matching": True
})
