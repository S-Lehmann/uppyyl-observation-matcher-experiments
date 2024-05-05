# Uppyyl Observation Matcher Experiments

The suite of observation matcher experiments conducted for the article "A model template for reachability-based containment checking of imprecise observations in timed automata" to be published in the international journal "Software and Systems Modeling" (SoSyM).

## Getting Started

In this section, you will find instructions to set up the Uppyyl Observation Matcher Experiments on your local machine.
The setup was tested in the [TACAS 23 Artifact Evaluation VM](https://zenodo.org/records/7113223).
For the setup in the TACAS 23 VM, execute the following steps:
- Add Network adapter: 
  - Settings -> Network -> Enable Network Adapter
- Add the VBoxGuestAdditions:
  - Settings -> Storage -> Controller: IDE -> "Add optical drive" button -> Select "VBoxGuestAdditions.iso"
  - In the VM: Open the mounted drive -> execute `./autorun.sh`
- Start the TACAS VM.
- Download Uppaal [version 4.1.24](https://uppaal.org/downloads/other/#uppaal-41) (or copy it into the VM using a shared folder).
- Create a folder in the VM under "Documents" were all data should be stored, and open a `cmd` there.
- Install Python3.8 (`sudo` may be required):
  - `add-apt-repository ppa:deadsnakes/ppa`
  - `apt-get install python3.8`
  - `apt-get install python3.8-distutils`
- Install and create virtualenv:
  - `python3.8 -m pip install virtualenv`
  - `export PATH=/home/tacas23/.local/bin:$PATH`
  - `virtualenv om-env`
- Clone the repositories (or copy them into the VM using a shared folder, `sudo` may be required):
  - `apt-get update`
  - `apt-get install git`
  - `git clone https://github.com/S-Lehmann/uppyyl-observation-matcher.git`
  - `git clone https://github.com/S-Lehmann/uppyyl-observation-matcher-experiments.git`
- Install the projects:
  - `python3.8 -m pip install -e ./uppyyl-observation-matcher/uppaal_c_language/`
  - `python3.8 -m pip install -e ./uppyyl-observation-matcher/uppaal_model/`
  - `python3.8 -m pip install -e ./uppyyl-observation-matcher/uppyyl_observation_matcher/`
  - `python3.8 -m pip install -e ./uppyyl-observation-matcher-experiments/`
- Set the correct path to the Uppaal bin directory:
  - Open `./uppyyl-observation-matcher-experiments/res/config.ini`
  - Set the `uppaal_dir_path`
- Execute the experiments:
  - `cd uppyyl-observation-matcher-experiments/`
  - `python3.8 -m uppyyl_observation_matcher_experiments`
  - `run`

### Prerequisites

#### Python

Install Python3.8 for this project.

#### Virtual Environment

If you want to install the project in a dedicated virtual environment, first install virtualenv:
```
python3.8 -m pip install virtualenv
```

And create a virtual environment:

```
cd project_folder
virtualenv om-env
```

Then, activate the virtual environment on macOS and Linux via:

```
source ./om-env/bin/activate
```

or on Windows via:

```
source .\om-env\Scripts\activate
```

#### Uppaal

The [Uppaal](https://www.uppaal.org/) model checking tool (tested with [version 4.1.24](https://uppaal.org/downloads/other/#uppaal-41)) is required to perform the actual checking on the generated matcher model.

#### Dependencies

Note that the experiments use the [Uppyyl Observation Matcher](https://github.com/S-Lehmann/uppyyl-observation-matcher) package, which needs to be installed beforehand.

### Installing

To install the Uppyyl Observation Matcher Experiments, run the following command:

```
python3.8 -m pip install -e path_to_uppyyl_observation_matcher_experiments
```

### Usage

To run the experiments CLI tool, first switch to the experiments project directory:

```
cd path_to_uppyyl_observation_matcher_experiments
```

Then, execute the following command:

```
python3.8 -m uppyyl_observation_matcher_experiments
```

Via the CLI, you can run all experiments via `run`, or specific experiments via `run exp_name` (e.g., `run exp.systematic.pos_and_neg_obs`)

### Experiments

The project suite contains the following experiment files (located in `uppyyl_observation_matcher_experiments/experiments`):

1. `introduction_example/introduction_example.py`: Contains the introductory example first described in the article section "Introduction" and later used in the section "Matcher model".
    * Inputs:
        - `res/example_models/introduction_example/main-example-model.xml`: The introduction model.
        - `res/example_models/introduction_example/observation.csv`: The example observation.
    * Outputs:
        - `logs/temp/models/main-example-model-TODO.xml`
    * Experiments:
        - `experiment_introduction_example()`: Matches the example observation with the full-featured matcher system derived from the introduction model.
    * Executed in the CLI tool via `run exp.examples.introduction`.

2. `systematic_experiments/systematic_experiments.py`: Contains the systematic experiments for correct classification of observations, and the comparison of matcher types, observation types, observation sizes, and observation extents.
    * Inputs:
        - The introduction model `main-example-model.xml` located in `res/example_models/introduction_example`
        - The experiment model suite (paths defined in `systematic_experiments/model_data.py`, models located in `res/uppaal_demo_models`)
            + Included models: `2doors.xml`, `bridge.xml`, `fischer.xml`, `fischer-symmetry.xml`, `interrupt.xml`, `train-gate.xml`, `train-gate-orig.xml`, `csmacd2.xml`, `tdma.xml`
    * Outputs:
        - Classification results, performance data
    * Experiments:
        1. `experiment_full_workflow_with_positive_and_negative_observations()`:
        Checks correctness of classification for positive and negative observations.
        Executed in the CLI tool via `run exp.systematic.pos_and_neg_obs`.
        2. `experiment_compare_performance_of_matcher_models()`:
        Compares matching run times for different matcher types ("R", "B", "BP", "BD", "BL", "BS", "BC", "BSC", and "All").
        Executed in the CLI tool via `run exp.systematic.matcher_types`.
        3. `experiment_compare_performance_of_observation_types()`:
        Compares matching run times for different observation types ("B", "P", "D", "L", "S", "C", "All").
        Executed in the CLI tool via `run exp.systematic.obs_types`.
        4. `experiment_compare_performance_of_observation_sizes()`:
        Compares matching run times for different observation sizes (between 1 and 200).
        Executed in the CLI tool via `run exp.systematic.obs_sizes`.
        5. `experiment_compare_performance_of_observation_extents()`:
        Compares matching run times for different observation extents (between 0 and 200).
        Executed in the CLI tool via `run exp.systematic.obs_extents`.

## Authors

* **Sascha Lehmann** - *Initial work* - [S-Lehmann](https://github.com/S-Lehmann)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* The Uppaal model checking tool can be found at https://www.uppaal.org/.
* The project is associated with the [Institute for Software Systems](https://www.tuhh.de/sts) at Hamburg University of Technology.
