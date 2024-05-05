"""The main entry point of the Uppaal observation matcher experiments module."""
import pathlib

from uppyyl_observation_matcher_experiments.backend.experiments.introduction_example.introduction_example import \
    experiment_introduction_example
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.helper_experiments import \
    HelperExperiments
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.systematic_experiments import \
    SystematicExperiments
from uppyyl_observation_matcher_experiments.definitions import RES_DIR


def main():
    """The main function."""
    experiment_base_dir_path = RES_DIR.parent.joinpath("logs/temp")  # pathlib.Path("/media/temp_disk/experiments")
    experiment_log_dir_path = RES_DIR.parent.joinpath("logs")

    ####################################
    # Helper Experiments
    ####################################
    _helper_experiments = HelperExperiments(
        experiment_base_dir_path=experiment_base_dir_path, experiment_log_dir_path=experiment_log_dir_path)
    # helper_experiments.experiment_generate_observations_for_exp_2()

    ####################################
    # Experiments
    ####################################
    systematic_experiments = SystematicExperiments(
        experiment_base_dir_path=experiment_base_dir_path, experiment_log_dir_path=experiment_log_dir_path)
    # experiment_introduction_example()
    # systematic_experiments.experiment_full_workflow_with_positive_and_negative_observations()
    # systematic_experiments.experiment_compare_performance_of_matcher_models()
    systematic_experiments.experiment_compare_performance_of_observation_types()
    # systematic_experiments.experiment_compare_performance_of_observation_sizes()
    # systematic_experiments.experiment_compare_performance_of_temporal_observation_extents()


if __name__ == '__main__':
    main()
