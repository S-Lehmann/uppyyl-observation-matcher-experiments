"""This module contains the introduction model example."""
import copy

from uppyyl_observation_matcher.backend.helper import load_model_from_file, get_instance_data
from uppyyl_observation_matcher.backend.observation.generator import ObservationGenerator
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.helper import \
    init_directories_and_paths, generate_and_save_preprocess_model
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.model_data import all_model_data
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.observation_configs import \
    base_observation_config


def pretty_print_dict(d, indent_per_level=4):
    """Pretty prints a given dict.

    Args:
        d: The dict to pretty print.
        indent_per_level: The concrete indentation used per indentation level.

    Returns:
        The pretty printed dict.
    """
    string = '{\n'
    string += pretty_print_dict_rec(d, indent=indent_per_level)
    string += '}'
    return string


def pretty_print_dict_rec(d, indent=0, indent_per_level=4):
    """Pretty prints a given dict recursively.

    Args:
        d: The dict to pretty print.
        indent: The current indentation level.
        indent_per_level: The concrete indentation used per indentation level.

    Returns:
        The pretty printed dict.
    """
    string = ""
    for key, value in d.items():
        string += ' ' * indent + f'"{key}": '
        if key in ["few-short", "many-short", "few-long", "many-long"]:
            string += '[\n'
            for data_point in value:
                string += ' ' * (indent + indent_per_level) + str(data_point) + ",\n"
            string += ' ' * indent + ']'
        elif isinstance(value, dict):
            string += "{\n"
            string += pretty_print_dict_rec(value, indent=indent + indent_per_level)
            string += ' ' * indent + "}"
        else:
            string += str(value)

        string += ",\n"

    return string


########################################################################################################################
# Experiment configurations #
########################################################################################################################

class HelperExperiments:
    """The helper experiments class."""

    def __init__(self, experiment_base_dir_path, experiment_log_dir_path=None):
        """Initializes HelperExperiments."""
        self.experiment_base_dir_path = experiment_base_dir_path
        self.experiment_log_dir_path = (experiment_log_dir_path if experiment_log_dir_path
                                        else self.experiment_base_dir_path.joinpath("logs"))

    ####################################################################################################################
    # Helper Experiment 1: Generate observations for experiment 2 #
    ####################################################################################################################
    def experiment_generate_observations_for_exp_2(self):
        """Generates fixed observations for experiment 2."""
        all_observation_data = {}
        for model_data in all_model_data[:]:
            model_name = model_data["path"].stem
            config = copy.deepcopy(base_observation_config)
            init_directories_and_paths(
                model_file_path=model_data["path"], output_dir_path=self.experiment_base_dir_path, config=config)

            config.update({
                "allow_variable_observations": True,
                "observed_variables": model_data["variables"],

                "allow_partial_observations": False,

                "default_deviation_bounds": (0, 0),
                "allowed_deviations_in_observations": {},

                "allow_location_observations": False,
                "observed_processes_for_locations": [],

                "time_shift_bounds": (0, 0),

                "allow_committed_observations": False,

                "concrete_transition_times": "min",  # min, max, random
                "force_keep_first_observation": False,
                "force_keep_last_observation": True,
            })

            # Prepare model
            input_model = load_model_from_file(model_path=config["original_model_file_path"])
            instance_data = get_instance_data(model=input_model, config=config)
            preprocessed_model = generate_and_save_preprocess_model(
                model=input_model, instance_data=instance_data, config=config)

            model_observation_data = {}

            # Generate "few-short" observation
            print(f'\n--- Generate "few-short" observation ---')
            config.update({
                "step_count": 10,
                "observation_count_bounds": (4, 4),
            })
            observation_generator = ObservationGenerator(config=config, model=preprocessed_model)
            observation_data = observation_generator.generate()
            model_observation_data["few-short"] = observation_data
            print(observation_data)

            # Generate "many-short" observation
            print(f'\n--- Generate "many-short" observation ---')
            config.update({
                "step_count": 10,
                "observation_count_bounds": (10, 10),
            })
            observation_generator = ObservationGenerator(config=config, model=preprocessed_model)
            observation_data = observation_generator.generate()
            model_observation_data["many-short"] = observation_data
            print(observation_data)

            # Generate "few-long" observation
            print(f'\n--- Generate "few-long" observation ---')
            config.update({
                "step_count": 40,
                "observation_count_bounds": (4, 4),
            })
            observation_generator = ObservationGenerator(config=config, model=preprocessed_model)
            observation_data = observation_generator.generate()
            model_observation_data["few-long"] = observation_data
            print(observation_data)

            # Generate "many-long" observation
            print(f'\n--- Generate "few-long" observation ---')
            config.update({
                "step_count": 40,
                "observation_count_bounds": (10, 10),
            })
            observation_generator = ObservationGenerator(config=config, model=preprocessed_model)
            observation_data = observation_generator.generate()
            model_observation_data["many-long"] = observation_data
            print(observation_data)

            all_observation_data[model_name] = model_observation_data

        print("=== Final data ===")
        pretty_string = "all_exp2_observation_data = " + pretty_print_dict(d=all_observation_data, indent_per_level=4)

        # Save data to file
        experiment_log_dir_path = self.experiment_log_dir_path.joinpath("helper")
        experiment_log_dir_path.mkdir(parents=True, exist_ok=True)
        experiment_log_file_path = experiment_log_dir_path.joinpath('exp2_observation_data.py')
        with open(experiment_log_file_path, 'w') as file:
            file.write(pretty_string)

