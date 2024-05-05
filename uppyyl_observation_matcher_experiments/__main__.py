"""The main entry point of the Uppaal observation matcher experiments module."""
from uppyyl_observation_matcher_experiments.cli.cli import UppaalObservationMatcherExperimentsCLI


def main():
    """The main function."""
    prompt = UppaalObservationMatcherExperimentsCLI()
    prompt.cmdloop()


if __name__ == '__main__':
    main()
