# Uppyyl Observation Matcher Experiments

The suite of observation matcher experiments conducted for the article "A model template for reachability-based containment checking of imprecise observations in timed automata" to be published in the international journal "Software and Systems Modeling" (SoSyM).

## Getting Started

In this section, you will find instructions to set up the Uppyyl Observation Matcher Experiments on your local machine.
The setup was tested in the [TACAS 23 Artifact Evaluation VM](https://zenodo.org/records/7113223).
For the setup in the TACAS 23 VM, execute the initial steps described in the first subsection of the prerequisites section;
otherwise, skip that part.

### Prerequisites

#### Initial setup of the TACAS 23 VM
**NOTE:**
The setup of Oracle VM VirtualBox might not work properly under MacOS/Arm64.
If that is the case, you can still try to install the experiments directly on your machine instead of using the TACAS VM.

- Download and install Oracle VM VirtualBox.
  - Note: For MacOS, only Intel hardware is fully supported yet.
- (MacOS only) Add a Host-only network adapter in the settings of VirtualBox.
- Download and import the [TACAS 23 Artifact Evaluation VM](https://zenodo.org/records/7113223) appliance.
- Enable the network adapter ("host-only" under MacOS):
  - Settings -> Network -> Enable Network Adapter
- (Optional) Add the VBoxGuestAdditions, e.g., for adapting the screen resolution in the VM:
  - See https://www.virtualbox.org/manual/ch04.html#guestadd-intro
- Start the TACAS VM
  - Username / Password: tacas23
- Create a folder in the VM under "Documents" were all data should be stored, and open a `cmd` there for the remaining setup steps.

#### Python

Install Python3.8 for this project (`sudo` may be required).
```
apt-get update
add-apt-repository ppa:deadsnakes/ppa
apt-get install python3.8
apt-get install python3.8-distutils
```

#### Git

Install any recent version of git (`sudo` may be required).
```
apt-get update
apt-get install git
```

#### Virtual Environment

If you want to install the project in a dedicated virtual environment, first install virtualenv (`sudo` may be required):
```
python3.8 -m pip install virtualenv
```

You may need to add the path to the virtualenv tool to the `PATH` environment variable:
```
export PATH=<path_to_bin_dir_with_virtualenv>:$PATH
(e.g., export PATH=/home/tacas23/.local/bin:$PATH)
```


Afterwards, create a virtual environment (`sudo` may be required):

```
cd <project_folder>
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

The experiments use the [Uppyyl Observation Matcher](https://github.com/S-Lehmann/uppyyl-observation-matcher) packages.

### Installing

**NOTE:**
Before installing the Uppyyl Observation Matcher Experiments, make sure that you successfully installed the [Uppyyl Observation Matcher](https://github.com/S-Lehmann/uppyyl-observation-matcher) packages (i.e., `uppaal_c_language`, `uppaal_model`, and `uppyyl_observation_matcher`) first, which provide the functionalities used in the experiments.

To install the Uppyyl Observation Matcher Experiments, first clone the repository:
```
cd <project_folder>
git clone https://github.com/S-Lehmann/uppyyl-observation-matcher-experiments.git
```

Then install the package with the following command (`sudo` may be required):

```
python3.8 -m pip install -e ./uppyyl-observation-matcher-experiments/
```


**NOTE:**
Out of the box, the experiments will be executed only for the example model developed in the journal article.
Some experiments also used a subset of the benchmark models included in the official [Uppaal](https://www.uppaal.org/) distribution.
To use the Uppaal demo model suite, copy the `2doors.xml`, `bridge.xml`, `fischer.xml`, `fischer-symmetry.xml`, `interrupt.xml`, `train-gate.xml`, and `train-gate-orig.xml` models to `./res/uppaal_demo_models`.
Furthermore, for the case-study-based models, copy the `csmacd2.xml` model (converted from [csma_input_02](https://www.it.uu.se/research/group/darts/uppaal/benchmarks/csma/csma_input_02.ta) to `xml` with Uppaal) and the `tdma.xml` model (described in detail in [[LP97]](https://www.it.uu.se/research/group/darts/papers/texts/lp-prfts97.pdf)) to `./res/uppaal_demo_models/case-study`.
In the `fischer.xml` and `fischer-symmetry.xml` models, change the value of the variable `N` to 3.
Also, add observable helper variables to the model `csmacd2.xml` if you want to use it in the experiment suite (in our experiments, we added the variables "t", "P0_state", "P1_state", and "P2_state").
To finally enable the models for the experiments, uncomment the corresponding model data under `uppyyl_observation_matcher_experiments/backend/experiments/systematic_experiments/model_data.py`.

### Usage

To run the experiments CLI tool, first set the correct path to the `bin` directory of Uppaal in the `config.ini` at `uppyyl-observation-matcher-experiments/res/config.ini`.
Afterwards, switch to the experiments project directory:

```
cd uppyyl-observation-matcher-experiments
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
