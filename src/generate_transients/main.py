"""
Script for generating transient lifetime data.
"""
from l96_ebm.deterministic.integrator import (
    L96_EBM_Integrator,
    L96_EBM_TrajectoryObserver,
)

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
    print("Opening Config\n")
    config = json.load(Path("cfg/transient_lifetime_130723.json").open())
    print("Opened Config")
    dt = config["dt"]
    integration_time = config["integration_time"]
    all_setups = config["all_setups"]
    setup = all_setups[input_number]
    file_name = config["results_file"]
    S, disapearing_attractor, ic_number = setup

    print(
        f"Running setup {input_number}/{len(all_setups)}. S={S:.3f}, ic {ic_number}.\n\n"
    )

    # Load IC
    ic = load_ic(disapearing_attractor, ic_number)

    # Run Integration
    print(f"Starting integration with ic={ic[-1]:.3f}, S={S}.\n\n")

    block_length = 1000
    number_of_observations = int(integration_time / dt)
    number_of_blocks = int(number_of_observations / block_length)

    runner = L96_EBM_Integrator(x_ic=ic[:-1], T_ic=ic[-1:], S=S)
    looker = L96_EBM_TrajectoryObserver(runner)

    for i in range(number_of_blocks):
        looker.make_observations(block_length, dt, timer=False)
        ds = looker.observations

        # Check if tipped/tipping time
        if tipped(ds):
            tipping_time = check_exit_time(ds, disapearing_attractor)
            log_result(file_name, S, disapearing_attractor, tipping_time)
            sys.exit(0)

    # Log nan if we reach integration end
    tipping_time = np.nan
    log_result(file_name, S, disapearing_attractor, tipping_time)
