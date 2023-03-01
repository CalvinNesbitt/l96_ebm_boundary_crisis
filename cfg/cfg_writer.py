"Script for writing config files"

import numpy as np
import itertools
from pathlib import Path
import json


if __name__ == "__main__":

    cfg_file = Path("cfg/longer_run.json")

    # W Setups
    w_S_values = np.linspace(7.7, 7.8, 10)
    w_setups = list(itertools.product(list(w_S_values), ["w"], range(0, 500)))

    # SB Setups
    sb_S_values = np.linspace(15.0, 15.2, 10)
    sb_setups = list(itertools.product(list(sb_S_values), ["sb"], range(0, 500)))

    all_setups = w_setups + sb_setups

    config = {
        "integration_time": 1.0e6,
        "dt": 0.1,
        "all_setups": all_setups,
        "results_file": "transient_lifetimes2.csv",
    }
    json.dump(config, cfg_file.open("w"))
