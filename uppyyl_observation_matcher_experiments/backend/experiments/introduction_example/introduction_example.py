"""This module contains the introduction model example."""
import copy

from uppyyl_observation_matcher.backend.helper import load_observation_data_from_csv, load_model_from_file, \
    get_instance_data
from uppyyl_observation_matcher.backend.matching import ObservationMatcher
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.helper import \
    generate_and_save_preprocess_model, init_directories_and_paths
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.matcher_model_configs import \
    all_matcher_model_configs
from uppyyl_observation_matcher_experiments.definitions import RES_DIR

experiment_sub_path = f'example_models/introduction_example'
experiment_input_folder = RES_DIR.joinpath(experiment_sub_path)
experiment_log_dir_path = RES_DIR.parent.joinpath("./logs")
main_config_path = RES_DIR.joinpath(f'config.ini')


def experiment_introduction_example():
    """Executes the experiments for the introduction model example."""
    config = copy.deepcopy(all_matcher_model_configs["All"])
    init_directories_and_paths(
        model_file_path=experiment_input_folder.joinpath("main-example-model.xml"),
        output_dir_path=experiment_log_dir_path.joinpath("introduction_example"),
        config=config
    )

    config.update({
        "csv_data_file_path": experiment_input_folder.joinpath("observation.csv"),
    })
    config.update({
        "allowed_deviations": {"t": 1, "db": 2, "temp": 100},
        "maximum_initial_delay": 20
    })

    run_timeout = 30

    # Prepare model
    input_model = load_model_from_file(model_path=config["original_model_file_path"])
    instance_data = get_instance_data(model=input_model, config=config)
    observation_data = load_observation_data_from_csv(
        csv_data_file_path=config["csv_data_file_path"], instance_data=instance_data)
    print(f'Observation data:\n{observation_data}')
    preprocessed_model = generate_and_save_preprocess_model(
        model=input_model, instance_data=instance_data, config=config)

    # Prepare trace matcher
    observation_matcher = ObservationMatcher(
        config=config, model=preprocessed_model, instance_data=instance_data,
        observation_data=None, matcher_type="All", timeout=run_timeout)
    observation_matcher.prepare_matcher_model()

    # Obtain matching trace
    matching_res = observation_matcher.match(
        observation_data=observation_data, return_trace=False, use_prepared=True)
    assert matching_res["is_matching"], f'No matching trace found even though one or more should match.'
