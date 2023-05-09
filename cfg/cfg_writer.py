"Script for writing config files"

import numpy as np
import itertools
from pathlib import Path
import json


if __name__ == "__main__":

    cfg_file = Path("cfg/transient_liftime_090523.json")

    w_S_values = np.linspace(7.8, 7.9, 50)
    w_setups = list(itertools.product(list(w_S_values), ["w"], range(0, 100)))

    # SB Setups
    sb_S_values = np.linspace(15.0, 14.9, 50)
    sb_setups = list(itertools.product(list(sb_S_values), ["sb"], range(0, 100)))

    all_setups = sb_setups + w_setups

    config = {
        "integration_time": 1.0e7,
        "dt": 0.1,
        "all_setups": all_setups,
        "results_file": "transient_liftime_090523.csv",
    }
    json.dump(config, cfg_file.open(mode="w"))
