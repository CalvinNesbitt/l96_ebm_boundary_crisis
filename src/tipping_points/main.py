"""
Script for determining where the tipping points are.
"""

from l96_ebm.deterministic.integrator import L96_EBM_Integrator, L96_EBM_TrajectoryObserver

from checker import tipped, check_exit_time
from logger import log_result, make_csv_file, results_file

import sys
import numpy as np

if __name__ == "__main__":

    input_number = int(sys.argv[1]) - 1  # so we can run in parallel

    if not results_file.exists():
        print(f"Making CSV file at {results_file.name}\n")
        make_csv_file()

    # Experiment setup
    sb_S_runs = np.repeat(np.arange(14.5, 15.6, 0.1), 10)  # do 10 ic for each S
    w_S_runs = np.repeat(np.arange(7.5, 8.6, 0.1), 10)
    all_S_runs = np.append(sb_S_runs, w_S_runs)
    S = all_S_runs[input_number]
    integration_time = 100.0
    dt = 0.1

    if S < 10:
        dissapearing_attractor = "w"
        T_ic = 300
    else:
        dissapearing_attractor = "sb"
        T_ic = 200

    # Run integration
    print(f"Running integration with T={T_ic:.3f}, S={S}.\n\n")
    runner = L96_EBM_Integrator(T_ic=T_ic, S=S)
    runner.time = 0
    looker = L96_EBM_TrajectoryObserver(runner)
    looker.make_observations(int(integration_time / dt), dt, timer=False)
    ds = looker.observations

    # Check if tipped/tipping time
    if tipped(ds):
        tipping_time = check_exit_time(ds)
    else:
        tipping_time = np.nan

    # Log Result
    log_result(S, dissapearing_attractor, tipping_time, input_number)
