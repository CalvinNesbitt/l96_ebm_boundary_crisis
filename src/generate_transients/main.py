"""
Script for generating transient lifetime data.
"""
from l96_ebm.deterministic.integrator import L96_EBM_Integrator, L96_EBM_TrajectoryObserver

from ic import load_ic
from exit_times import tipped, check_exit_time
from logger import log_result

import sys
import json
import numpy as np
from pathlib import Path

if __name__ == "__main__":
    # Load Run
    input_number = int(sys.argv[1]) - 1
    config = json.load(Path("cfg/transient_liftime_090523-TEST.json").open())
    print(config)
    dt = config["dt"]
    integration_time = config["integration_time"]
    all_setups = config["all_setups"]
    setup = all_setups[input_number]
    file_name = config["results_file"]
    S, disapearing_attractor, ic_number = setup

    print(f"Running setup {input_number}/{len(all_setups)}. S={S:.3f}, ic {ic_number}.\n\n")

    # Load IC
    ic = load_ic(disapearing_attractor, ic_number)

    # Run Integration
    print(f"Starting integration with ic={ic[-1]:.3f}, S={S}.\n\n")
    runner = L96_EBM_Integrator(x_ic=ic[:-1], T_ic=ic[-1:], S=S)
    looker = L96_EBM_TrajectoryObserver(runner)
    looker.make_observations(int(integration_time / dt), dt, timer=False)
    ds = looker.observations

    # Check if tipped/tipping time
    if tipped(ds):
        tipping_time = check_exit_time(ds, disapearing_attractor)
    else:
        tipping_time = np.nan

    # Save transient lifetime
    log_result(file_name, S, disapearing_attractor, tipping_time)
