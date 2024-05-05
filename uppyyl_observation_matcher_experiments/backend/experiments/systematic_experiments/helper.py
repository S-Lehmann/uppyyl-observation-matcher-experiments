"""A set of helper functions."""

import pathlib

from uppyyl_observation_matcher.backend.helper import save_model_to_file
from uppyyl_observation_matcher.backend.transformer.model.concrete.preprocessed_model_transformer import \
    PreprocessedModelTransformer


def init_directories_and_paths(model_file_path, output_dir_path, config):
    """Initializes the directories and paths used during the experiments.

    Args:
        model_file_path: The path of the model file.
        output_dir_path: The path of the output directory.
        config: The configuration dict which should contain the new path data.
    """
    temp_data_dir_path = output_dir_path.joinpath("temp")
    model_output_dir_path = temp_data_dir_path.joinpath("models")
    trace_output_dir_path = temp_data_dir_path.joinpath("traces")

    model_output_dir_path.mkdir(parents=True, exist_ok=True)
    trace_output_dir_path.mkdir(parents=True, exist_ok=True)

    model_name = pathlib.Path(model_file_path.stem)
    config.update({
        "output_dir_path": output_dir_path,
        "temp_data_dir_path": temp_data_dir_path,
        "model_output_dir_path": model_output_dir_path,
        "trace_output_dir_path": trace_output_dir_path,

        "original_model_file_path": model_file_path,
        "preprocessed_model_file_path": model_output_dir_path.joinpath(f'{model_name}_preprocessed.xml'),
        "matcher_model_file_path": model_output_dir_path.joinpath(f'{model_name}_matcher.xml'),
        "random_trace_generator_model_file_path": model_output_dir_path.joinpath(f'{model_name}_trace-generator.xml'),
        "transition_simulator_model_file_path": model_output_dir_path.joinpath(
            f'{model_name}_transition-simulator.xml'),
        "details_model_file_path": model_output_dir_path.joinpath(f'{model_name}_details.xml'),

        "matcher_model_trace_file_path": trace_output_dir_path.joinpath(f'{model_name}_matcher-trace-1.xml'),
        "random_trace_file_path": trace_output_dir_path.joinpath(f'{model_name}_random-trace-1.xml'),
        "transition_simulator_trace_file_path": trace_output_dir_path.joinpath(f'{model_name}_simulated-trace-1.xml'),
        "details_model_trace_file_path": trace_output_dir_path.joinpath(f'{model_name}_details-trace-1.xml'),
    })


def generate_and_save_preprocess_model(model, instance_data, config):
    """Generates the preprocessed model from the source model and saves it.

    Args:
        model: The source model.
        instance_data: The instance data of the source model.
        config: The configuration dict containing path data.

    Returns:
        The preprocessed model.
    """
    preprocessed_model_transformer = PreprocessedModelTransformer()
    preprocessed_model_transformer.set_instance_data(instance_data=instance_data)
    preprocessed_model = model.copy()
    preprocessed_model_transformer.transform(model=preprocessed_model)
    save_model_to_file(model=preprocessed_model, model_path=config["preprocessed_model_file_path"])
    return preprocessed_model
