"Function to check if a given integration tipped."

import numpy as np


def tipped(ds):
    "Function to check if a given integration tipped."
    T_timeseries = ds.T.values
    hot_at_some_point = np.any(T_timeseries > 270)
    cold_at_some_point = np.any(T_timeseries < 270)
    return cold_at_some_point * hot_at_some_point


# Functions to check exit times


def check_w_exit_time(ds, lb=272.28):
    T_timeseries = ds.T.values
    exit_index = T_timeseries.shape[0] - np.argmax(np.flip(T_timeseries > lb))
    return ds.time[exit_index].item()


def check_sb_exit_time(ds, ub=267.66):
    T_timeseries = ds.T.values
    exit_index = T_timeseries.shape[0] - np.argmax(np.flip(T_timeseries < ub))
    return ds.time[exit_index].item()


def check_exit_time(ds, disappearing_attractor: str):
    if disappearing_attractor == "sb":
        return check_sb_exit_time(ds)
    if disappearing_attractor == "w":
        return check_w_exit_time(ds)
