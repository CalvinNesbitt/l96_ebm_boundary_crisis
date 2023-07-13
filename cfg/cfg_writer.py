"Script for writing config files"

import numpy as np
import itertools
from pathlib import Path
import json


if __name__ == "__main__":
    cfg_file = Path("cfg/transient_lifetime_130723_BIG.json")

    # SB Setups
    sb_S_values = np.linspace(15.35, 15.45, 10)
    sb_setups = list(itertools.product(list(sb_S_values), ["sb"], range(0, 500)))

    # W Setups
    w_S_values = np.linspace(7.7, 7.8, 10)
    w_setups = list(itertools.product(list(w_S_values), ["w"], range(0, 500)))

    all_setups = sb_setups + w_setups

    config = {
        "integration_time": 1.0e6,
        "dt": 0.25,
        "all_setups": all_setups,
        "results_file": "/rds/general/user/cfn18/home/Thesis-Computing/Determinisitc/l96_ebm_boundary_crisis/data/transient_lifetime_130723_BIG.csv",
    }
    json.dump(config, cfg_file.open(mode="w"))
