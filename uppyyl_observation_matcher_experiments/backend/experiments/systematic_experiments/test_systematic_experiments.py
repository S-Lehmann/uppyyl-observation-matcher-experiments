"""This module contains the introduction example experiment as test."""
import pathlib

import pytest

from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.systematic_experiments import \
    SystematicExperiments
from uppyyl_observation_matcher_experiments.definitions import RES_DIR


##########
# Helper #
##########
def print_header(text):
    """Prints a header line for an experiment.

    Args:
        text: The header text.

    Returns:
        The header line.
    """
    main_line = f'=== {text} ==='
    highlight_line = '=' * len(main_line)
    header = f'{highlight_line}\n{main_line}\n{highlight_line}'
    print(header)

    return header


@pytest.fixture(scope="module")
def experiments():
    """A fixture for an Experiments instance.

    Returns:
        The Experiments instance.
    """
    experiment_base_dir_path = pathlib.Path("/media/temp_disk/experiments")
    experiment_log_dir_path = RES_DIR.parent.joinpath("./logs")

    systematic_experiments = SystematicExperiments(
        experiment_base_dir_path=experiment_base_dir_path, experiment_log_dir_path=experiment_log_dir_path)
    return systematic_experiments


################################################################################
# Experiments #
################################################################################

def test_experiment_full_workflow_with_positive_and_negative_observations(experiments):
    print_header("Checks correctness of classification for positive and negative observations")
    experiments.experiment_full_workflow_with_positive_and_negative_observations()


def test_experiment_compare_performance_of_matcher_models(experiments):
    print_header("Compares matching run times for different matcher types")
    experiments.experiment_compare_performance_of_matcher_models()


def test_experiment_compare_performance_of_observation_types(experiments):
    print_header("Compares matching run times for different observation types")
    experiments.experiment_compare_performance_of_observation_types()


def test_experiment_compare_performance_of_observation_sizes(experiments):
    print_header("Compares matching run times for different observation sizes")
    experiments.experiment_compare_performance_of_observation_sizes()


def test_experiment_compare_performance_of_observation_extents(experiments):
    print_header("Compares matching run times for different observation extents")
    experiments.experiment_compare_performance_of_observation_extents()
