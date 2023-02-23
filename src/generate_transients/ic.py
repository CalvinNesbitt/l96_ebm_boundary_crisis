"""
Code for generating ic for our transients. At each tipping point we define a box around the attractor 
"""
# Custom Code
from l96_ebm.deterministic.utils.i_o import get_attractor

from i_o import transient_ic_dir

# Standard Packages
import numpy as np
import numpy.random as rm


# Functions for generating ic files


def determine_bounds(attractor):
    attractor_np = attractor.ds_as_np
    lower_bounds = np.min(attractor_np, axis=0)
    upper_bounds = np.max(attractor_np, axis=0)
    return lower_bounds, upper_bounds


def get_sample_ic_from_bounding_box(attractor, number_of_samples):
    "Fetches samples from a box."
    lb, ub = determine_bounds(attractor)
    return rm.uniform(lb, ub, size=(number_of_samples, attractor.ndim))


# Functions for loading ic files
def load_ic(disapearing_attractor, ic_number):
    if disapearing_attractor == "sb":
        return np.load(transient_ic_dir / "sb_ic.npy")[ic_number]
    elif disapearing_attractor == "w":
        return np.load(transient_ic_dir / "w_ic.npy")[ic_number]


# Script for generating ic
if __name__ == "__main__":

    number_of_ic = 1000
    # Specify Tipping Points
    S_sb_to_w = 14.9  # just before the SB attractor disappears
    # S_w_to_sb = 8.1  # just before the W attractor disappears
    sb_attractor = get_attractor(S_sb_to_w, "sb")
    # w_attractor = get_attractor(S_w_to_sb, "w")
    sb_ic = get_sample_ic_from_bounding_box(sb_attractor, number_of_ic)
    # w_ic = get_sample_ic_from_bounding_box(w_attractor, number_of_ic)

    # np.save(transient_ic_dir / "w_ic", w_ic)
    np.save(transient_ic_dir / "sb_ic", sb_ic)
