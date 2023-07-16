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
from loguru import logger

if __name__ == "__main__":
    # Load Run
    input_number = int(sys.argv[1]) - 1
    logger.info("Opening Config\n")
    config = json.load(Path("cfg/transient_lifetime_better_ic.json").open())
    logger.info("Opened Config")
    dt = config["dt"]
    integration_time = config["integration_time"]
    all_setups = config["all_setups"]
    setup = all_setups[input_number]
    file_name = config["results_file"]
    S, disapearing_attractor, ic_number = setup

    logger.info(
        f"Running setup {input_number + 1}/{len(all_setups)}. S={S:.3f}, ic {ic_number}.\n\n"
    )

    # Load IC
    ic = load_ic(disapearing_attractor)

    # Run Integration
    logger.info(f"Starting integration with ic={ic[-1]:.3f}, S={S}.\n\n")

    block_length = 1000
    number_of_blocks = int(integration_time / block_length)

    runner = L96_EBM_Integrator(x_ic=ic[:-1], T_ic=ic[-1:], S=S)
    looker = L96_EBM_TrajectoryObserver(runner)

    for i in range(number_of_blocks):
        looker.make_observations(int(block_length / dt), dt, timer=False)
        ds = looker.observations

        # Check if tipped/tipping time
        if tipped(ds):
            tipping_time = check_exit_time(ds, disapearing_attractor)
            log_result(file_name, S, disapearing_attractor, tipping_time)
            sys.exit(0)

    # Log nan if we reach integration end
    tipping_time = np.nan
    log_result(file_name, S, disapearing_attractor, tipping_time)
