"""
Module for analysing transient lifetime data.
"""

from thesis_plots.core import init_2d_fax

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd


def exponential_pdf(x, decay_rate):
    return decay_rate * np.exp(-decay_rate * x)


def data_vs_exponential_pdf_plot(data_points, fax=None, **kwargs):
    if fax is None:
        fax = init_2d_fax()
    fig, ax = fax

    # Get mean and std
    mean = np.mean(data_points)
    decay_rate = 1 / mean

    # Plot theoretical pdf
    data_grid = np.linspace(0, max(data_points), 100)
    ax.plot(
        data_grid,
        exponential_pdf(data_grid, decay_rate),
        label="Theoretical Distribution",
        c="k",
    )

    # Bin data to get empirical pdf
    n_bins = int(len(data_points) / 100)
    ax.hist(data_points, bins=n_bins, density=True, **kwargs)
    counts, bin_edges = np.histogram(data_points, bins=n_bins, density=True)
    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
    ax.scatter(bin_centres, counts, label="Empirical Distribution", c="r", marker="o")
    ax.set_yscale("log")
    return fig, ax


def lifetime_scaling_law(S, critical_exponent, tipping_point, y_intercept):
    "Computes log of mean lifetime as a function of S"
    distance_from_tipping_point = np.abs(S - tipping_point)
    log_mean_lifetime = np.log(y_intercept) - critical_exponent * np.log(
        distance_from_tipping_point
    )
    return log_mean_lifetime


def inverse_lifetime_scaling_law(
    mean_lifetime, critical_exponent, tipping_point, y_intercept
):
    "Computes log of mean lifetime as a function of S"
    distance_from_tipping_point = np.exp(
        (np.log(y_intercept) - np.log(mean_lifetime)) / critical_exponent
    )
    return distance_from_tipping_point


def fit_from_data(
    S_values,
    mean_lifetimes,
    initial_critical_exponent,
    initial_tipping_point,
    initial_y_intercept,
):
    "Use curve fit to find scaling law from data"
    log_mean_lifetimes = np.log(mean_lifetimes)
    tipping_point_bounds = (initial_tipping_point - 1, initial_tipping_point + 1)
    params, cov = curve_fit(
        lifetime_scaling_law,
        S_values,
        log_mean_lifetimes,
        p0=[initial_critical_exponent, initial_tipping_point, initial_y_intercept],
        bounds=(
            [0, min(tipping_point_bounds), 1.0e-8],
            [15, max(tipping_point_bounds), 100],
        ),
    )

    def log_lifetime_function(S):
        return lifetime_scaling_law(S, *params)

    return log_lifetime_function, params, cov


def plot_of_fit(S_values, mean_lifetimes, log_lifetime_function, params, cov, fax=None):
    "Plots fit and data"
    if fax is None:
        fig, ax = init_2d_fax()
    else:
        fig, ax = fax
    S_grid = np.linspace(min(S_values), max(S_values), 100)
    S_critical = params[1]
    distance_from_tip = np.abs(S_grid - S_critical)
    ax.plot(
        np.log(distance_from_tip),
        log_lifetime_function(S_grid),
        label="Fit",
        ls="--",
        c="k",
    )
    ax.scatter(
        np.log(np.abs(S_values - S_critical)),
        np.log(mean_lifetimes),
        label="Observations",
    )
    ax.set_xlabel("$\log(|S - S_c|)$")
    ax.set_ylabel("$\log(\\tau)$")
    ax.set_title("Fit of scaling law to data")
    ax.legend()
    return fig, ax


class TransientLifetimeResult:
    "Class for plotting result"

    def __init__(self, df: pd.DataFrame, dissapearing_attractor: str):
        # Filter Dataframe
        df = df[["S", "dissapearing_attractor", "tipping_time"]]
        self.df = df[df.dissapearing_attractor == dissapearing_attractor]
        self.df.dropna(inplace=True)

        # Make sure we have at least 100 samples for a given S
        self.df = self.df.groupby("S").filter(lambda x: len(x) > 100)

        # Compute derived values
        self.dissapearing_attractor = dissapearing_attractor
        self.mean_lifetimes = self.df.groupby("S").mean(numeric_only=True).tipping_time
        self.S_values = self.mean_lifetimes.index.values.flatten()
        # sort S values
        self.S_values.sort()

        if self.dissapearing_attractor == "sb":
            self.fit_scaling_law(6, 14.9, 1.0e-2)
        if self.dissapearing_attractor == "w":
            self.fit_scaling_law(6, 7.9, 1.0e-2)

    def plot_mean_tipping_time(self, fax=None):
        if fax is None:
            fig, ax = init_2d_fax()
        else:
            fig, ax = fax
        ax.plot(self.S_values, self.mean_lifetimes, marker="o")
        ax.set_xlabel("$S$")
        ax.set_ylabel("$\log(\\tau)$")
        ax.set_title("Mean Transient Lifetimes")
        ax.set_yscale("log")
        return fig, ax

    def tipping_times(self, S):
        # If S is within 1.e-3 of a value in S_values, use that value
        nearest_S = self.S_values[np.argmin(np.abs(self.S_values - S))]
        if np.abs(nearest_S - S) > 1.0e-4:
            raise ValueError(f"S={S} not in S_values")
        df = self.df[self.df["S"] == nearest_S].tipping_time
        df.S = nearest_S
        return df

    def tipping_time_histogram(self, S, fax=None, **kwargs):
        if fax is None:
            fax = init_2d_fax()
        fig, ax = fax
        fig, ax = data_vs_exponential_pdf_plot(self.tipping_times(S), fax=fax, **kwargs)
        ax.set_title(f"Transient Lifetimes PDF, S={S:.2f}")
        ax.set_xlabel("Transient Lifetime")
        ax.set_ylabel("$\\rho$")
        ax.grid()
        return fig, ax

    def tipping_time_histogram_list(self, index, fax=None):
        fig, ax = self.tipping_time_histogram(self.S_values[index], fax=fax)
        return fig, ax

    def all_tipping_time_histograms(self, **kwargs):
        # Make grid of axes
        n_rows = int(np.sqrt(len(self.S_values)))
        # ceiling function
        n_cols = int(np.ceil(len(self.S_values) / n_rows))

        fig, axs = plt.subplots(n_rows, n_cols, figsize=(20, 15))
        axs = axs.flatten()
        for _, S in enumerate(self.S_values):
            self.tipping_time_histogram(S, fax=(fig, axs[_]), **kwargs)
            axs[_].set_title(f"S={S:.2f}")

        # Only keep x labels on outer axes
        for _, ax in enumerate(axs):
            if _ < len(axs) - n_cols:
                ax.set_xlabel("")
            if _ % n_cols != 0:
                ax.set_xlabel("")
        # Only keep y labels on outer axes
        for _, ax in enumerate(axs):
            if _ % n_cols != 0:
                ax.set_ylabel("")

        fig.tight_layout()
        return fig, axs

    def fit_scaling_law(
        self, initial_critical_exponent, initial_tipping_point, initial_y_intercept
    ):
        log_lifetime_function, params, cov = fit_from_data(
            self.S_values,
            self.mean_lifetimes,
            initial_critical_exponent,
            initial_tipping_point,
            initial_y_intercept,
        )
        self.log_lifetime_function = log_lifetime_function
        self.params = params
        self.critical_exponent = params[0]
        self.tipping_point = params[1]
        self.y_intercept = params[2]
        self.cov = cov
        self.tipping_point_err = np.sqrt(self.cov[1, 1])
        self.critical_exponent_err = np.sqrt(self.cov[0, 0])
        return

    def plot_scaling_lawfit(self, fax=None):
        fig, ax = plot_of_fit(
            self.S_values,
            self.mean_lifetimes,
            self.log_lifetime_function,
            self.params,
            self.cov,
            fax=fax,
        )

        if self.dissapearing_attractor == "sb":
            sc_label = "S_{SB \\to W}"
        if self.dissapearing_attractor == "w":
            sc_label = "S_{W \\to SB}"
        ax.set_title(
            f"${sc_label} = {self.tipping_point:.2f}\pm{self.tipping_point_err:.2f}$, $\\gamma = {self.critical_exponent:.2f}\pm{self.critical_exponent_err:.2f}$"
        )
        ax.set_xlabel(f"$\log(|S - {sc_label}|)$")
        return fig, ax

    def estimate_S_from_tau(self, tau):
        distance_from_S_c = inverse_lifetime_scaling_law(tau, *self.params)
        if self.dissapearing_attractor == "sb":
            S = self.tipping_point + distance_from_S_c
        if self.dissapearing_attractor == "w":
            S = self.tipping_point - distance_from_S_c
        return S

    def plot_number_of_samples(self, fax=None):
        if fax is None:
            fig, ax = init_2d_fax()
        else:
            fig, ax = fax
        ax.scatter(self.S_values, self.df.groupby("S").count().tipping_time)
        ax.set_xlabel("$S$")
        ax.set_ylabel("Number of samples")
        ax.set_title("Number of samples vs S")
        return fig, ax
