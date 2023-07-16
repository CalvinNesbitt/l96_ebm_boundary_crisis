"""
Code for generating ic for our transients.
"""
# Custom Code
from l96_ebm.deterministic.integrator import L96_EBM_Integrator

from i_o import transient_ic_dir

# Standard Packages
import numpy as np
import numpy.random as rm


# Functions for generating ic files


def generate_random_ic(S, attractor):
    if attractor == "sb":
        T_ic = 200 + rm.uniform(-10, 10)
    elif attractor == "w":
        T_ic = 300 + rm.uniform(-10, 10)

    runner = L96_EBM_Integrator(T_ic=T_ic, S=S)
    runner.run(500)
    return runner.state


# Functions for loading ic files
def load_ic(disapearing_attractor):
    if disapearing_attractor == "sb":
        S = 14.85
    elif disapearing_attractor == "w":
        S = 7.95
    return generate_random_ic(S, disapearing_attractor)
