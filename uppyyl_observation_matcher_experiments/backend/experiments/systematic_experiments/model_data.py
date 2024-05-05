"""This module contains the models data for the state construction experiments."""
from uppyyl_observation_matcher_experiments.definitions import RES_DIR

all_model_data = [
    # Example models
    {"path": RES_DIR.joinpath("example_models/introduction_example/main-example-model.xml"),
     "variables": ["t", "db", "temp"]},

    # Supported Uppaal demo models
    {"path": RES_DIR.joinpath("uppaal_demo_models/2doors.xml"),
     "variables": ["t", "activated1", "activated2"]},
    {"path": RES_DIR.joinpath("uppaal_demo_models/bridge.xml"),
     "variables": ["t", "L"]},
    {"path": RES_DIR.joinpath("uppaal_demo_models/fischer.xml"),
     "variables": ["t", "id"]},  # Note: Changed N from 6 to 3 for performance reasons
    {"path": RES_DIR.joinpath("uppaal_demo_models/fischer-symmetry.xml"),
     "variables": ["t", "set", "id"]},   # Note: Changed N from 10 to 3 for performance reasons
    {"path": RES_DIR.joinpath("uppaal_demo_models/interrupt.xml"),
     "variables": ["t", "count"]},
    {"path": RES_DIR.joinpath("uppaal_demo_models/train-gate.xml"),
     "variables": ["t", "Gate_Tmpl_len"]},
    {"path": RES_DIR.joinpath("uppaal_demo_models/train-gate-orig.xml"),
     "variables": ["t", "el", "Queue_Tmpl_len", "Queue_Tmpl_i"]},

    # Additional case study models
    {"path": RES_DIR.joinpath("uppaal_demo_models/case-study/csmacd2.xml"),
     "variables": ["t", "P0_state", "P1_state", "P2_state"]},  # Note: Added observable helper variables
    {"path": RES_DIR.joinpath("uppaal_demo_models/case-study/tdma.xml"),
     "variables": ["t", "busid", "n"]},

    # Unsupported models
    # {"path": RES_DIR.joinpath("uppaal_demo_models/unsupported/scheduling3.xml"),
    #  "variables": []},
    # {"path": RES_DIR.joinpath("uppaal_demo_models/unsupported/scheduling4.xml"),
    #  "variables": []},
    # {"path": RES_DIR.joinpath("uppaal_demo_models/unsupported/SchedulingFramework.xml"),
    #  "variables": []},
]
