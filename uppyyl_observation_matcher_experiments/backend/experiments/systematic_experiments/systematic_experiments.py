"""This module contains the introduction model example."""
import copy
import json

from uppyyl_observation_matcher.backend.helper import load_model_from_file, get_instance_data
from uppyyl_observation_matcher.backend.matching import ObservationMatcher
from uppyyl_observation_matcher.backend.observation.generator import ObservationGenerator
from uppyyl_observation_matcher.backend.trace.simulator import EdgeTraceSimulator
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.matcher_model_configs import \
    base_matcher_model_config, all_matcher_model_configs
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.helper import \
    init_directories_and_paths, generate_and_save_preprocess_model
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.model_data import all_model_data
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.exp2_observation_data import \
    all_exp2_observation_data
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.observation_configs import \
    all_observation_configs, base_observation_config
from uppyyl_observation_matcher_experiments.backend.helper import calculate_min_max_avg_float


########################################################################################################################
# Experiment configurations #
########################################################################################################################
class SystematicExperiments:
    """The systematic experiments class."""

    def __init__(self, experiment_base_dir_path, experiment_log_dir_path=None):
        """Initializes SystematicExperiments."""
        self.experiment_base_dir_path = experiment_base_dir_path
        self.experiment_log_dir_path = (experiment_log_dir_path if experiment_log_dir_path
                                        else self.experiment_base_dir_path.joinpath("logs"))

    ####################################################################################################################
    # Experiment 1: Execute full workflow with positive and negative observations #
    ####################################################################################################################
    def experiment_full_workflow_with_positive_and_negative_observations(self):
        """Executes the experiment for correctness of positive and negative observation matching."""
        positive_run_count = 10  # 1000
        negative_run_count = 10  # 1000
        run_timeout = 30
        step_count = 20

        max_deviation = 5
        max_initial_delay = 10

        indexed_model_data = list(enumerate(all_model_data, 1))
        for model_idx, model_data in indexed_model_data[0:8]:
            model_name = model_data["path"].stem
            config = copy.deepcopy(all_matcher_model_configs["All"])
            init_directories_and_paths(
                model_file_path=model_data["path"], output_dir_path=self.experiment_base_dir_path, config=config)

            matcher_model_name = f'{model_name}_exp1_matcher'
            observed_variables = model_data["variables"]

            config.update({
                "matcher_model_file_path": config["model_output_dir_path"].joinpath(
                    f'{matcher_model_name}.xml'),
                "allowed_deviations": dict([(v, max_deviation) for v in observed_variables]),
                "maximum_initial_delay": max_initial_delay,
            })

            config.update(all_observation_configs["All"])
            config.update({
                "step_count": step_count,
                "observation_count_bounds": (10, 10),
                "observed_variables": observed_variables,
                "force_keep_first_observation": True,
                "force_keep_last_observation": True,
            })

            # Prepare model
            input_model = load_model_from_file(model_path=config["original_model_file_path"])
            instance_data = get_instance_data(model=input_model, config=config)
            preprocessed_model = generate_and_save_preprocess_model(
                model=input_model, instance_data=instance_data, config=config)

            # Prepare trace generator, matcher, and edge trace simulator
            observation_generator = ObservationGenerator(config=config, model=preprocessed_model)
            observation_matcher = ObservationMatcher(
                config=config, model=preprocessed_model, instance_data=instance_data,
                observation_data=None, matcher_type="All", timeout=run_timeout)
            observation_matcher.prepare_matcher_model()
            edge_trace_simulator = EdgeTraceSimulator(
                config=config, model=preprocessed_model, instance_data=instance_data
            )

            # Perform "n" runs with the current model and different randomized positive observation data
            positive_runs_log_data = {}
            for run_idx in range(0, positive_run_count):
                run_log_data = {
                    "durations": {}, "obs_data": [], "is_matching": False, "is_simulated": False,
                    "is_included": False
                }
                print(
                    f'\n--- Execute positive run {run_idx + 1} / {positive_run_count} of model "{model_name}" ---')
                observation_data = observation_generator.generate()
                run_log_data["obs_data"] = observation_data
                print(f'Observation data:\n{observation_data}')

                # Obtain matching trace
                matching_res = observation_matcher.match(
                    observation_data=observation_data, return_trace=True, use_prepared=True,
                    log_time_to=(run_log_data["durations"], f'matching'))
                run_log_data["is_matching"] = matching_res["is_matching"]
                run_log_data["is_timeout"] = matching_res["is_timeout"]
                matched_trace = matching_res["matching_trace"]
                assert matching_res["is_matching"], f'No matching trace found even though one or more should match.'

                # Re-simulate matching trace edges
                edge_trace = [tr.triggered_edges for tr in matched_trace.transitions]
                is_simulated, simulated_trace = edge_trace_simulator.simulate_edge_trace(
                    edge_trace=edge_trace)
                run_log_data["is_simulated"] = is_simulated
                assert is_simulated, f'Matching edge trace could not be simulated on the original model.'

                # Check if the matching trace is included in the re-simulated trace
                is_included = simulated_trace.includes(trace=matched_trace)
                run_log_data["is_included"] = is_included
                assert is_included, \
                    f'The simulated trace does not include the matched trace:\n\n' \
                    f'Simulated trace:\n{simulated_trace}\n\n' \
                    f'Matched trace:\n{matched_trace}\n\n' \
                    f'Observation data:\n{observation_data}'

                positive_runs_log_data[run_idx] = run_log_data

            config.update({
                "allow_partial_observations": False,
            })

            # Perform "n" runs with the current model and different randomized negative observation data
            negative_runs_log_data = {}
            for run_idx in range(0, negative_run_count):
                run_log_data = {
                    "durations": {}, "obs_data": [], "is_matching": False
                }
                print(
                    f'\n--- Execute negative run {run_idx + 1} / {negative_run_count} of model "{model_name}" ---')
                observation_data = observation_generator.generate_negative()
                run_log_data["obs_data"] = observation_data
                print(f'Observation data:\n{observation_data}')

                # Check that no matching trace exists
                matching_res = observation_matcher.match(
                    observation_data=observation_data, return_trace=True, use_prepared=True,
                    log_time_to=(run_log_data["durations"], f'matching'))
                run_log_data["is_matching"] = matching_res["is_matching"]
                run_log_data["is_timeout"] = matching_res["is_timeout"]
                matched_trace = matching_res["matching_trace"]
                assert not matching_res["is_matching"], \
                    f'Matching trace found even though none should match.\n\n ' \
                    f'Matched trace:\n{matched_trace}\n\n' \
                    f'Observation data:\n{observation_data}'

                negative_runs_log_data[run_idx] = run_log_data

            model_log_data = {model_name: {
                "positives": positive_runs_log_data,
                "negatives": negative_runs_log_data
            }}

            # Save data to file
            experiment_log_dir_path = self.experiment_log_dir_path.joinpath('exp1_pos_neg_runs')
            experiment_log_dir_path.mkdir(parents=True, exist_ok=True)
            experiment_log_file_path = experiment_log_dir_path.joinpath(f'exp1_{model_idx:02}_{model_name}_log.json')
            with open(experiment_log_file_path, 'w') as file:
                json.dump(model_log_data, file, sort_keys=False, separators=(',', ':'))

    ####################################################################################################################
    # Experiment 2: Compare performance of matcher models #
    ####################################################################################################################
    def experiment_compare_performance_of_matcher_models(self):
        """Executes the experiment for comparing the performance of different matcher versions.

        The following model versions are compared:
        1) The raw matcher model before simplification and without any extensions.
        2) The basic (i.e., simplified) matcher model without any extensions.
        3) The basic matcher model with partial observation matching.
        4) The basic matcher model with deviating observation matching.
        5) The basic matcher model with location observation matching.
        6) The basic matcher model with shifted observation matching.
        7) The basic matcher model with committed observation matching.
        8) The basic matcher model with shifted and committed observation matching
            (i.e., with different shifting section for committed locations).
        9) The basic matcher model with all 5 extensions applied simultaneously
            (i.e., the most complex matcher).
        """

        runs_per_scenario = 10  # 100
        run_timeout = 30

        # experiment_log_data = {}
        indexed_model_data = list(enumerate(all_model_data, 1))
        for model_idx, model_data in indexed_model_data[:]:
            config = copy.deepcopy(base_matcher_model_config)
            init_directories_and_paths(model_file_path=model_data["path"],
                                       output_dir_path=self.experiment_base_dir_path, config=config)

            input_model = load_model_from_file(model_path=config["original_model_file_path"])
            instance_data = get_instance_data(model=input_model, config=config)
            preprocessed_model = generate_and_save_preprocess_model(
                model=input_model, instance_data=instance_data, config=config)

            model_name = model_data["path"].stem
            model_log_data = {}
            model_obs_data = all_exp2_observation_data[model_name]
            for obs_type, obs_data in model_obs_data.items():
                obs_log_data = {}
                for matcher_type, matcher_model_config in all_matcher_model_configs.items():
                    # Insert dummy "None" data into the log when no observation data is provided
                    if not obs_data:
                        obs_log_data[matcher_type] = {
                            "runs": None,
                            "summary": {}
                        }
                        continue

                    # Adapt the configuration for the concrete observation type
                    config.update(matcher_model_config)
                    matcher_model_name = f'{model_name}_{matcher_type.replace("+", "_")}'
                    config["matcher_model_file_path"] = config["model_output_dir_path"].joinpath(
                        f'{matcher_model_name}.xml')

                    # Prepare the observation matcher
                    observation_matcher = ObservationMatcher(
                        config=config, model=preprocessed_model, instance_data=instance_data,
                        observation_data=obs_data, matcher_type=matcher_type, timeout=run_timeout)
                    observation_matcher.create_matcher_model()

                    # Execute runs
                    runs_log_data = {}
                    for run_idx in range(0, runs_per_scenario):
                        print(f'Run {run_idx + 1} ...')
                        run_log_data = {"durations": {}, "is_matching": False}

                        matching_res = observation_matcher.match(
                            return_trace=False, use_existing_matcher=True,
                            log_time_to=(run_log_data["durations"], f'matching'))
                        assert (matching_res["is_matching"] or matching_res["is_timeout"]), \
                            f'No matching trace found even though one or more should match.'

                        run_log_data["is_matching"] = matching_res["is_matching"]
                        run_log_data["is_timeout"] = matching_res["is_timeout"]

                        runs_log_data[run_idx] = run_log_data

                    # Obtain derived values
                    scenario_matching_durations = [run_log["durations"]["matching"]["matching"] for
                                                   run_log in runs_log_data.values()]
                    min_max_avg_durations = calculate_min_max_avg_float(scenario_matching_durations)

                    # Gather data
                    obs_log_data[matcher_type] = {
                        "runs": runs_log_data,
                        "summary": {
                            "min_max_avg": min_max_avg_durations
                        }
                    }

                    print(f'Exp2 -> Model: {model_name}, obs-type: {obs_type}, matcher-type: {matcher_type} => '
                          f'{obs_log_data[matcher_type]["summary"]["min_max_avg"]}')
                model_log_data[obs_type] = obs_log_data

            # Save data to file
            stored_model_log_data = {model_name: model_log_data}
            experiment_log_dir_path = self.experiment_log_dir_path.joinpath('exp2_matcher_models')
            experiment_log_dir_path.mkdir(parents=True, exist_ok=True)
            experiment_log_file_path = experiment_log_dir_path.joinpath(f'exp2_{model_idx:02}_{model_name}_log.json')
            with open(experiment_log_file_path, 'w') as file:
                json.dump(stored_model_log_data, file, sort_keys=False, separators=(',', ':'))

    ####################################################################################################################
    # Experiment 3: Compare performance of observation types #
    ####################################################################################################################
    def experiment_compare_performance_of_observation_types(self):
        """Executes the experiment for comparing the performance of matching simple and complex observation types.

        The following observation types are compared:
        1) Basic observations, i.e., full and exact observations.
        2) Partial observations, i.e., observations where individual variables
            are not observed in individual data points.
        3) Deviating observations, i.e., observations where individual variable values
            deviate from the actual values.
        4) Location observations, i.e., observations where model locations are observed in addition.
        5) Time-shifted observations, i.e., observations whose time stamps are shifted compared to the model clock time.
        6) Committed observations, i.e., observations where committed states are also observable.
        7) Advanced observations which combine all aforementioned traits.
        """

        runs_per_scenario = 10  # 100
        run_timeout = 30
        step_count = 20

        max_deviation = 5
        max_initial_delay = 10

        indexed_model_data = list(enumerate(all_model_data, 1))
        for model_idx, model_data in indexed_model_data[:]:
            model_name = model_data["path"].stem
            model_base_config = copy.deepcopy(all_matcher_model_configs["All"])
            init_directories_and_paths(
                model_file_path=model_data["path"], output_dir_path=self.experiment_base_dir_path,
                config=model_base_config)

            matcher_model_name = f'{model_name}_exp3_matcher'
            observed_variables = model_data["variables"]

            model_base_config.update({
                "matcher_model_file_path": model_base_config["model_output_dir_path"].joinpath(
                    f'{matcher_model_name}.xml'),
                "allowed_deviations": dict([(v, max_deviation) for v in observed_variables]),
                "maximum_initial_delay": max_initial_delay,
            })

            model_log_data = {}
            for obs_type, obs_config in all_observation_configs.items():
                # Update config
                config = copy.deepcopy(model_base_config)
                config.update(obs_config)
                config.update({
                    "step_count": step_count,
                    "observation_count_bounds": (10, 10),
                    "observed_variables": observed_variables,
                    "force_keep_first_observation": True,
                    "force_keep_last_observation": True,
                })

                # Prepare model
                input_model = load_model_from_file(model_path=config["original_model_file_path"])
                instance_data = get_instance_data(model=input_model, config=config)
                preprocessed_model = generate_and_save_preprocess_model(
                    model=input_model, instance_data=instance_data, config=config)

                # Prepare trace generator, matcher, and edge trace simulator
                observation_generator = ObservationGenerator(config=config, model=preprocessed_model)
                observation_matcher = ObservationMatcher(
                    config=config, model=preprocessed_model, instance_data=instance_data,
                    observation_data=None, matcher_type="All", timeout=run_timeout)
                observation_matcher.prepare_matcher_model()

                runs_log_data = {}
                for run_idx in range(0, runs_per_scenario):
                    print(
                        f'\n--- Execute run {run_idx + 1} / {runs_per_scenario} of model "{model_name}" '
                        f'(obs type: "{obs_type}") ---')
                    run_log_data = {"durations": {}, "obs_data": [], "is_matching": False}

                    observation_data = observation_generator.generate()
                    print(f'Observation data:\n{observation_data}')

                    matching_res = observation_matcher.match(
                        observation_data=observation_data, return_trace=False, use_prepared=True,
                        log_time_to=(run_log_data["durations"], f'matching'))
                    assert (matching_res["is_matching"] or matching_res["is_timeout"]), \
                        f'No matching trace found even though one or more should match.'

                    run_log_data["is_matching"] = matching_res["is_matching"]
                    run_log_data["is_timeout"] = matching_res["is_timeout"]
                    run_log_data["obs_data"] = observation_data

                    runs_log_data[run_idx] = run_log_data

                scenario_matching_durations = [run_log["durations"]["matching"]["matching"] for
                                               run_log in runs_log_data.values()]
                model_log_data[obs_type] = {
                    "runs": runs_log_data,
                    "summary": {
                        "min_max_avg": calculate_min_max_avg_float(scenario_matching_durations)
                    }
                }

                print(f'Exp3 -> Model: {model_name}, obs-type: {obs_type}, matcher-type: All => '
                      f'{model_log_data[obs_type]["summary"]["min_max_avg"]}')

                # Save data to file
                stored_model_log_data = {model_name: model_log_data}
                experiment_log_dir_path = self.experiment_log_dir_path.joinpath('exp3_obs_types')
                experiment_log_dir_path.mkdir(parents=True, exist_ok=True)
                experiment_log_file_path = experiment_log_dir_path.joinpath(
                    f'exp3_{model_idx:02}_{model_name}_log.json')
                with open(experiment_log_file_path, 'w') as file:
                    json.dump(stored_model_log_data, file, sort_keys=False, separators=(',', ':'))

    ####################################################################################################################
    # Experiment 4: Compare performance of observation sizes #
    ####################################################################################################################
    def experiment_compare_performance_of_observation_sizes(self):
        """Executes the experiment for comparing the performance of matching different observation sizes."""

        runs_per_scenario = 5  # 20
        run_timeout = 30
        step_count = 200
        observation_count_step_size = 10  # 5

        indexed_model_data = list(enumerate(all_model_data, 1))
        for model_idx, model_data in indexed_model_data[1:]:
            model_name = model_data["path"].stem
            config = copy.deepcopy(all_matcher_model_configs["All"])
            init_directories_and_paths(
                model_file_path=model_data["path"], output_dir_path=self.experiment_base_dir_path, config=config)

            matcher_model_name = f'{model_name}_exp4_matcher'
            observed_variables = model_data["variables"]

            config.update({
                "matcher_model_file_path": config["model_output_dir_path"].joinpath(
                    f'{matcher_model_name}.xml'),
                "allowed_deviations": {},
                "maximum_initial_delay": 0,
            })

            config.update(base_observation_config)
            config.update({
                "step_count": step_count,
                "observed_variables": observed_variables,
                "force_keep_first_observation": False,
                "force_keep_last_observation": True,
            })

            model_log_data = {}
            observation_counts = list(range(1, step_count+2, observation_count_step_size))
            for obs_count in observation_counts:
                # Update config
                config.update({
                    "observation_count_bounds": (obs_count, obs_count),
                })

                # Prepare model
                input_model = load_model_from_file(model_path=config["original_model_file_path"])
                instance_data = get_instance_data(model=input_model, config=config)
                preprocessed_model = generate_and_save_preprocess_model(
                    model=input_model, instance_data=instance_data, config=config)

                # Prepare trace generator, matcher, and edge trace simulator
                observation_generator = ObservationGenerator(config=config, model=preprocessed_model)
                observation_matcher = ObservationMatcher(
                    config=config, model=preprocessed_model, instance_data=instance_data,
                    observation_data=None, matcher_type="All", timeout=run_timeout)
                observation_matcher.prepare_matcher_model()

                runs_log_data = {}
                for run_idx in range(0, runs_per_scenario):
                    print(
                        f'\n--- Execute run {run_idx + 1} / {runs_per_scenario} of model "{model_name}" '
                        f'(obs-count: {obs_count}) ---')
                    run_log_data = {"durations": {}, "obs_data": [], "is_matching": False}

                    observation_data = observation_generator.generate()
                    print(f'Observation data:\n{observation_data}')

                    matching_res = observation_matcher.match(
                        observation_data=observation_data, return_trace=False, use_prepared=True,
                        log_time_to=(run_log_data["durations"], f'matching'))
                    assert (matching_res["is_matching"] or matching_res["is_timeout"]), \
                        f'No matching trace found even though one or more should match.'

                    run_log_data["is_matching"] = matching_res["is_matching"]
                    run_log_data["is_timeout"] = matching_res["is_timeout"]
                    run_log_data["obs_data"] = observation_data

                    runs_log_data[run_idx] = run_log_data

                scenario_matching_durations = [run_log["durations"]["matching"]["matching"] for
                                               run_log in runs_log_data.values()]
                model_log_data[obs_count] = {
                    "runs": runs_log_data,
                    "summary": {
                        "min_max_avg": calculate_min_max_avg_float(scenario_matching_durations)
                    }
                }

                print(f'Exp4 -> Model: {model_name}, obs-count: {obs_count}, matcher-type: All => '
                      f'{model_log_data[obs_count]["summary"]["min_max_avg"]}')

                # Save data to file
                stored_model_log_data = {model_name: model_log_data}
                experiment_log_dir_path = self.experiment_log_dir_path.joinpath('exp4_obs_size')
                experiment_log_dir_path.mkdir(parents=True, exist_ok=True)
                experiment_log_file_path = experiment_log_dir_path.joinpath(
                    f'exp4_{model_idx:02}_{model_name}_log.json')
                with open(experiment_log_file_path, 'w') as file:
                    json.dump(stored_model_log_data, file, sort_keys=False, separators=(',', ':'))

    ####################################################################################################################
    # Experiment 5: Compare performance of temporal observation extents #
    ####################################################################################################################
    def experiment_compare_performance_of_observation_extents(self):
        """Executes the experiment for comparing the performance of matching different observation extents."""

        runs_per_scenario = 5  # 20
        run_timeout = 30

        max_step_count = 200
        step_count_step_size = 10  # 5
        observation_count = 10

        indexed_model_data = list(enumerate(all_model_data, 1))
        for model_idx, model_data in indexed_model_data[:]:
            model_name = model_data["path"].stem
            config = copy.deepcopy(all_matcher_model_configs["All"])
            init_directories_and_paths(
                model_file_path=model_data["path"], output_dir_path=self.experiment_base_dir_path, config=config)

            matcher_model_name = f'{model_name}_exp5_matcher'
            observed_variables = model_data["variables"]

            config.update({
                "matcher_model_file_path": config["model_output_dir_path"].joinpath(
                    f'{matcher_model_name}.xml'),
                "allowed_deviations": {},
                "maximum_initial_delay": 0,
            })

            config.update(base_observation_config)
            config.update({
                "observed_variables": observed_variables,
                "observation_count_bounds": (observation_count, observation_count),
                "force_keep_first_observation": True,
                "force_keep_last_observation": True,
            })

            model_log_data = {}
            step_counts = list(range(observation_count, max_step_count+1, step_count_step_size))
            for step_count in step_counts:
                # Update config
                config.update({
                    "step_count": step_count,
                })

                # Prepare model
                input_model = load_model_from_file(model_path=config["original_model_file_path"])
                instance_data = get_instance_data(model=input_model, config=config)
                preprocessed_model = generate_and_save_preprocess_model(
                    model=input_model, instance_data=instance_data, config=config)

                # Prepare trace generator, matcher, and edge trace simulator
                observation_generator = ObservationGenerator(config=config, model=preprocessed_model)
                observation_matcher = ObservationMatcher(
                    config=config, model=preprocessed_model, instance_data=instance_data,
                    observation_data=None, matcher_type="All", timeout=run_timeout)
                observation_matcher.prepare_matcher_model()

                runs_log_data = {}
                for run_idx in range(0, runs_per_scenario):
                    print(
                        f'\n--- Execute run {run_idx + 1} / {runs_per_scenario} of model "{model_name}" '
                        f'(step-count: {step_count}) ---')
                    run_log_data = {"durations": {}, "obs_data": [], "is_matching": False}

                    observation_data = observation_generator.generate()
                    print(f'Observation data:\n{observation_data}')

                    matching_res = observation_matcher.match(
                        observation_data=observation_data, return_trace=False, use_prepared=True,
                        log_time_to=(run_log_data["durations"], f'matching'))
                    assert (matching_res["is_matching"] or matching_res["is_timeout"]), \
                        f'No matching trace found even though one or more should match.'

                    run_log_data["is_matching"] = matching_res["is_matching"]
                    run_log_data["is_timeout"] = matching_res["is_timeout"]
                    run_log_data["obs_data"] = observation_data

                    runs_log_data[run_idx] = run_log_data

                scenario_matching_durations = [run_log["durations"]["matching"]["matching"] for
                                               run_log in runs_log_data.values()]
                model_log_data[step_count] = {
                    "runs": runs_log_data,
                    "summary": {
                        "min_max_avg": calculate_min_max_avg_float(scenario_matching_durations)
                    }
                }

                print(f'Exp5 -> Model: {model_name}, step-count: {step_count}, matcher-type: All => '
                      f'{model_log_data[step_count]["summary"]["min_max_avg"]}')

                # Save data to file
                stored_model_log_data = {model_name: model_log_data}
                experiment_log_dir_path = self.experiment_log_dir_path.joinpath('exp5_obs_extents')
                experiment_log_dir_path.mkdir(parents=True, exist_ok=True)
                experiment_log_file_path = experiment_log_dir_path.joinpath(
                    f'exp5_{model_idx:02}_{model_name}_log.json')
                with open(experiment_log_file_path, 'w') as file:
                    json.dump(stored_model_log_data, file, sort_keys=False, separators=(',', ':'))
