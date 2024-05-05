"""This module provides all plot functions for the DBM state construction experiments."""

import json
import os
import pprint
import pathlib

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator
from matplotlib.font_manager import FontProperties

pp = pprint.PrettyPrinter(indent=4, compact=True)

########################################################################################################################
# Experiment configurations #
########################################################################################################################
output_dir_path = pathlib.Path("/media/temp_disk/experiments")
output_data_dir_path = output_dir_path.joinpath("log")


def load_all_model_data_from_folder(data_folder):
    """Loads all existing model data found in a given folder.

    Args:
        data_folder: The data folder.

    Returns:
        All loaded model data.
    """
    data_file_names = [f for f in sorted(os.listdir(data_folder)) if os.path.isfile(os.path.join(data_folder, f))]

    all_model_data = {}
    for data_file_name_with_ext in data_file_names:
        data_file_name = os.path.splitext(data_file_name_with_ext)[0]
        model_num, model_name = tuple(data_file_name.split("_", maxsplit=1))

        data_file_path = f'{data_folder}/{data_file_name_with_ext}'
        with open(data_file_path, 'r') as file:
            all_model_data[model_name] = json.load(file)

    return all_model_data


################################################################################

class Plots:
    """The main experiments plot class."""

    def __init__(self, experiment_log_dir_path, plot_output_dir_path):
        """Initializes Plots."""
        self.experiment_log_dir_path = experiment_log_dir_path
        self.plot_output_dir_path = plot_output_dir_path

    ####################################################################################################################
    # Experiment 1: Execute full workflow with positive and negative observations #
    ####################################################################################################################
    def create_csv_file_for_positive_and_negative_runs(
            self, all_data=None, save_plot=False, show_plot=False):
        """Creates a CSV file for the data on positive and negative runs.

        Args:
            all_data: All model details.
            save_plot: Choose whether the generated plot should be saved.
            show_plot: Choose whether the generated plot should be shown.
        """
        experiment_data_path = self.experiment_log_dir_path.joinpath('exp1_pos_neg_runs')
        plot_output_dir_path = self.plot_output_dir_path.joinpath('exp1_pos_neg_runs')
        if all_data is None:
            all_data = {}
            file_paths = sorted([f for f in pathlib.Path(experiment_data_path).iterdir() if f.is_file()])
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    all_data.update(data)

        csv_data = [["modelname", "true_pos", "false_pos", "true_neg", "false_neg"]]
        for model_name, model_runs_data in all_data.items():
            model_details_row = [
                model_name,
                str(len([run for run in model_runs_data["positives"].values() if run["is_included"]])),
                str(len([run for run in model_runs_data["positives"].values() if not run["is_included"]])),
                str(len([run for run in model_runs_data["negatives"].values() if not run["is_matching"]])),
                str(len([run for run in model_runs_data["negatives"].values() if run["is_matching"]])),
            ]
            csv_data.append(model_details_row)

        csv_str = "\n".join(list(map(lambda row_: ";".join(row_), csv_data)))

        if show_plot:
            print(csv_str)
        if save_plot:
            plot_output_dir_path.mkdir(parents=True, exist_ok=True)

            output_csv_file_path = plot_output_dir_path.joinpath('exp1_data_table.csv')
            with open(output_csv_file_path, 'w') as file:
                file.write(csv_str)
            print(f'File "{output_csv_file_path}" saved.')

    ####################################################################################################################
    # Experiment 2: Compare performance of matcher models #
    ####################################################################################################################
    def create_latex_table_for_compare_performance_of_matcher_models(
            self, all_data=None, save_plot=False, show_plot=False):
        """Creates a LaTeX table for the comparison of matcher model performances.

        Args:
            all_data: All model details.
            save_plot: Choose whether the generated plot should be saved.
            show_plot: Choose whether the generated plot should be shown.
        """
        experiment_data_path = self.experiment_log_dir_path.joinpath('exp2_matcher_models')
        plot_output_dir_path = self.plot_output_dir_path.joinpath('exp2_matcher_models')
        if all_data is None:
            all_data = {}
            file_paths = sorted([f for f in pathlib.Path(experiment_data_path).iterdir() if f.is_file()])
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    all_data.update(data)
        scenario_names = list(list(all_data.values())[0]["few-short"].keys())

        # Create CSV data
        csv_data = [["modelname", "obs_type"] + list(map(lambda name: name.replace("+", ""), scenario_names))]
        for model_name, model_log_data in all_data.items():
            for obs_type, obs_log_data in model_log_data.items():
                model_details_row = [model_name, obs_type]
                for scenario_name, scenario_log_data in obs_log_data.items():
                    min_max_avg = scenario_log_data["summary"]["min_max_avg"]
                    if min_max_avg:
                        model_details_row.append(f'{min_max_avg[2]:.3f}')
                    else:
                        model_details_row.append('-')
                csv_data.append(model_details_row)

        csv_str = "\n".join(list(map(lambda row_: ";".join(row_), csv_data)))

        if show_plot:
            print(csv_str)
        if save_plot:
            plot_output_dir_path.mkdir(parents=True, exist_ok=True)

            output_csv_file_path = plot_output_dir_path.joinpath('exp2_data_table.csv')
            with open(output_csv_file_path, 'w') as file:
                file.write(csv_str)
            print(f'File "{output_csv_file_path}" saved.')

        # Create LaTeX data
        latex_data = []
        longest_model_name = max(map(lambda name: (name, len(name)), all_data.keys()), key=lambda v: v[1])[0]
        first_cell_max_length = len(f'\\multirow{{4}}*{{\\texttt{{{longest_model_name}}}}}')
        for model_name, model_log_data in all_data.items():
            latex_model_data = []
            first_cell = f'\\multirow{{4}}*{{\\texttt{{{model_name}}}}}'
            for obs_idx, (obs_type, obs_log_data) in enumerate(model_log_data.items()):
                latex_row_data = []
                if obs_idx == 0:
                    latex_row_data.append(first_cell + " " * (first_cell_max_length - len(first_cell)))
                else:
                    latex_row_data.append(" " * first_cell_max_length)
                latex_row_data.append(f'\\texttt{{{obs_type.replace("-", ",")}}}')
                for scenario_name, scenario_log_data in obs_log_data.items():
                    min_max_avg = scenario_log_data["summary"]["min_max_avg"]
                    if min_max_avg:
                        latex_row_data.append(f'${min_max_avg[2]:.3f}$')
                    else:
                        latex_row_data.append('$-$')
                latex_model_data.append(latex_row_data)
            latex_data.append(latex_model_data)

        latex_model_strs = []
        for latex_model_data in latex_data:
            latex_model_strs.append("\n".join(list(map(lambda row_: " & ".join(row_) + f' \\\\', latex_model_data))) +
                                    "\\hline")
        latex_str = "\n".join(latex_model_strs)

        if show_plot:
            print(latex_str)
        if save_plot:
            plot_output_dir_path.mkdir(parents=True, exist_ok=True)

            output_latex_file_path = plot_output_dir_path.joinpath('exp2_latex_table_data.tex')
            with open(output_latex_file_path, 'w') as file:
                file.write(latex_str)
            print(f'File "{output_latex_file_path}" saved.')

    ####################################################################################################################
    # Experiment 3: Compare performance of observation types #
    ####################################################################################################################
    def create_latex_table_for_compare_performance_of_observation_types(
            self, all_data=None, save_plot=False, show_plot=False):
        """Creates a LaTeX table for the comparison of observation type performances.

        Args:
            all_data: All model details.
            save_plot: Choose whether the generated plot should be saved.
            show_plot: Choose whether the generated plot should be shown.
        """
        experiment_data_path = self.experiment_log_dir_path.joinpath('exp3_obs_types')
        plot_output_dir_path = self.plot_output_dir_path.joinpath('exp3_obs_types')
        if all_data is None:
            all_data = {}
            file_paths = sorted([f for f in pathlib.Path(experiment_data_path).iterdir() if f.is_file()])
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    all_data.update(data)
        scenario_names = list(list(all_data.values())[0].keys())

        # Create CSV data
        csv_data = [["modelname"] + scenario_names]
        for model_name, model_log_data in all_data.items():
            model_details_row = [model_name]
            for obs_type, obs_log_data in model_log_data.items():
                min_max_avg = obs_log_data["summary"]["min_max_avg"]
                if min_max_avg:
                    model_details_row.append(f'{min_max_avg[2]:.3f}')
                else:
                    model_details_row.append('-')
            csv_data.append(model_details_row)

        csv_str = "\n".join(list(map(lambda row_: ";".join(row_), csv_data)))

        if show_plot:
            print(csv_str)
        if save_plot:
            plot_output_dir_path.mkdir(parents=True, exist_ok=True)

            output_csv_file_path = plot_output_dir_path.joinpath('exp3_data_table.csv')
            with open(output_csv_file_path, 'w') as file:
                file.write(csv_str)
            print(f'File "{output_csv_file_path}" saved.')

        # Create LaTeX data
        latex_data = []

        longest_model_name = max(map(lambda name: (name, len(name)), all_data.keys()), key=lambda v: v[1])[0]
        first_cell_max_length = len(f'\\texttt{{{longest_model_name}}}')
        for model_name, model_log_data in all_data.items():
            latex_model_data = []
            first_cell = f'\\texttt{{{model_name}}}'
            latex_model_data.append(first_cell + " " * (first_cell_max_length - len(first_cell)))
            for obs_type, obs_log_data in model_log_data.items():
                min_max_avg = obs_log_data["summary"]["min_max_avg"]
                if min_max_avg:
                    latex_model_data.append(f'${min_max_avg[2]:.3f}$')
                else:
                    latex_model_data.append('$-$')
            latex_data.append(latex_model_data)

        latex_str = "\n".join(list(map(lambda row_: " & ".join(row_) + f' \\\\\\hline', latex_data)))

        if show_plot:
            print(latex_str)
        if save_plot:
            plot_output_dir_path.mkdir(parents=True, exist_ok=True)

            output_latex_file_path = plot_output_dir_path.joinpath('exp3_latex_table_data.tex')
            with open(output_latex_file_path, 'w') as file:
                file.write(latex_str)
            print(f'File "{output_latex_file_path}" saved.')

    ####################################################################################################################
    # Experiment 4+5: Compare performance of observation sizes and extents #
    ####################################################################################################################
    def create_plot_for_compare_performance_of_observation_sizes_and_extents(
            self, all_data=None, save_plot=False, show_plot=False):
        """Creates a LaTeX table for the comparison of observation type performances.

        Args:
            all_data: All model details.
            save_plot: Choose whether the generated plot should be saved.
            show_plot: Choose whether the generated plot should be shown.
        """
        experiment_4_data_path = self.experiment_log_dir_path.joinpath('exp4_obs_size')
        experiment_5_data_path = self.experiment_log_dir_path.joinpath('exp5_obs_extents')
        plot_output_dir_path = self.plot_output_dir_path.joinpath('exp_obs_size_obs_extents')
        if all_data is None:
            all_data = {
                "exp4_obs_size": {},
                "exp5_obs_extents": {}
            }
            file_paths = sorted([f for f in pathlib.Path(experiment_4_data_path).iterdir() if f.is_file()])
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    all_data["exp4_obs_size"].update(data)
            file_paths = sorted([f for f in pathlib.Path(experiment_5_data_path).iterdir() if f.is_file()])
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    all_data["exp5_obs_extents"].update(data)

        # plt.clf()
        dpi = 300
        plt.figure(figsize=(1920 / dpi, 1080 / dpi), dpi=dpi)
        # plt.figure(figsize=(1920 / dpi, 1080 / dpi), dpi=dpi)

        markersize = 2
        font_p = FontProperties()
        font_p.set_size(8)

        # plt.subplots_adjust(hspace=1, top=0.8)

        # LEFT PLOT (observation sizes)
        ax_left = plt.subplot(1, 2, 1)

        for model_name, measure_data in all_data["exp4_obs_size"].items():
            x_vals = [int(x) for x in measure_data.keys()]
            y_vals = list(map(lambda measure: measure["summary"]["min_max_avg"][2], measure_data.values()))
            _model_plot, = ax_left.plot(x_vals, y_vals, 'x-', markersize=markersize, markeredgewidth=0.5, linewidth=1,
                                        label=f'"{model_name}"')

        ax_left.set_xlabel('observation size')
        ax_left.set_ylabel('average matching time [s]')

        ax_left.legend(bbox_to_anchor=(-0.27, -0.2, 2.65, -0.1), loc="upper left", mode="expand", borderaxespad=0,
                       ncol=5, prop=font_p, handletextpad=0.3)
        ax_left.grid(which='both', alpha=0.5)
        ax_left.set_yscale("log")
        ax_left.set_xlim(-2, 202)  # 102
        ax_left.set_ylim(0.01, 35)

        def update_yticks(y, _pos):
            """Updates the ticks on the y-axis.

            Args:
                y: The y value.
                _pos: The position of the tick.

            Returns:
                The string representation of the updated tick.
            """
            if y in [0.01, 0.1]:
                return str(y)
            elif y in [1, 10, 30]:
                return str(int(y))
            else:
                return ""

        ax_left.xaxis.set_major_locator(MultipleLocator(40))
        ax_left.yaxis.set_minor_formatter(FuncFormatter(update_yticks))
        ax_left.yaxis.set_major_formatter(FuncFormatter(update_yticks))
        ax_left.get_yaxis().set_tick_params(which='minor', pad=5)

        # RIGHT PLOT (observation extents)
        ax_right = plt.subplot(1, 2, 2)

        for model_name, measure_data in all_data["exp5_obs_extents"].items():
            x_vals = [int(x) for x in measure_data.keys()]
            y_vals = list(map(lambda measure: measure["summary"]["min_max_avg"][2], measure_data.values()))
            _model_plot, = ax_right.plot(x_vals, y_vals, 'x-', markersize=markersize, markeredgewidth=0.5, linewidth=1,
                                         label=f'"{model_name}"')

        ax_right.set_xlabel('transition count')
        ax_right.set_ylabel('average matching time [s]')

        ax_right.grid(which='both', alpha=0.5)
        ax_right.set_yscale("log")
        ax_right.set_xlim(8, 202)  # 102
        ax_right.set_ylim(0.01, 35)

        def update_yticks(y, _pos):
            """Updates the ticks on the y-axis.

            Args:
                y: The y value.
                _pos: The position of the tick.

            Returns:
                The string representation of the updated tick.
            """
            if y in [0.01, 0.1]:
                return str(y)
            elif y in [1, 10, 30]:
                return str(int(y))
            else:
                return ""

        ax_right.xaxis.set_major_locator(MultipleLocator(40))
        ax_right.yaxis.set_minor_formatter(FuncFormatter(update_yticks))
        ax_right.yaxis.set_major_formatter(FuncFormatter(update_yticks))
        ax_right.get_yaxis().set_tick_params(which='minor', pad=5)

        plt.tight_layout()
        if save_plot:
            plot_output_dir_path.mkdir(parents=True, exist_ok=True)

            output_file_path = plot_output_dir_path.joinpath('exp4-exp5-obs-sizes-and-extents.png')
            plt.savefig(output_file_path, dpi=300)
            print(f'File "{output_file_path}" saved.')
        if show_plot:
            plt.show()
