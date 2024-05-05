"""The main entry point of the Uppaal observation matcher experiments plot module."""
from uppyyl_observation_matcher_experiments.backend.experiments.systematic_experiments.plots import Plots

from uppyyl_observation_matcher_experiments.definitions import RES_DIR


def main():
    """The main function."""
    experiment_log_dir_path = RES_DIR.parent.joinpath("logs")
    plot_output_dir_path = experiment_log_dir_path.joinpath("plots")

    ####################################
    # Plots
    ####################################
    plots = Plots(experiment_log_dir_path=experiment_log_dir_path, plot_output_dir_path=plot_output_dir_path)
    plots.create_csv_file_for_positive_and_negative_runs(save_plot=True, show_plot=True)
    plots.create_latex_table_for_compare_performance_of_matcher_models(save_plot=True, show_plot=True)
    plots.create_latex_table_for_compare_performance_of_observation_types(save_plot=True, show_plot=True)
    plots.create_plot_for_compare_performance_of_observation_sizes_and_extents(save_plot=True, show_plot=True)


if __name__ == '__main__':
    main()
