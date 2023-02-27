import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

from calvin_stats.computations import linear_regression_fit
from calvin_stats.plots import linear_regression_plot, init_2d_fax


class TransientLifetimes:
    "Class for handing transient lifetime data. Can plot critical exponent fit."

    def __init__(self, csv_file, dissapearing_attractor, S_crit):
        self.file = csv_file
        self.dissapearing_attractor = dissapearing_attractor
        self.ds = self.load_ds(csv_file, dissapearing_attractor, S_crit)
        self.default_S_list = self.ds.S.unique()

    def observations(self, S_list=[]):
        if len(S_list) == 0:
            S_list = self.default_S_list
        return self.ds[self.ds.S.isin(S_list)]

    def load_ds(self, csv_file, dissapearing_attractor, S_crit):
        ds = pd.read_csv(csv_file)[["S", "dissapearing_attractor", "tipping_time"]]
        ds.S_crit = S_crit
        ds["distance_from_crit"] = (ds.S - S_crit).abs()
        return ds[ds["dissapearing_attractor"] == dissapearing_attractor].reset_index()[
            ["S", "distance_from_crit", "tipping_time"]
        ]

    def mean_lifetimes(self, S_list=[]):
        "Returns a dataset of the mean transient lifetimes"
        ds = self.observations(S_list).copy()
        # ds['mean_tipping_time'] = ds.groupby('S').transform('mean')['tipping_time']
        mean_ds = pd.DataFrame()
        mean_ds["distance_from_crit"] = ds.groupby("S").mean()["distance_from_crit"]
        mean_ds["mean_tipping_time"] = ds.groupby("S").mean()["tipping_time"]
        mean_ds["error"] = ds.groupby("S").mean()["tipping_time"] / ds.groupby("S").count()["tipping_time"]
        return mean_ds

    def critical_exponent_fit_plot(self, S_list=[], fax=None):

        # Get mean lifetimes
        ds = self.mean_lifetimes(S_list=S_list)
        distance_from_crit = ds.distance_from_crit
        log_distance_from_crit = np.log(distance_from_crit)
        mean_tipping_time = ds.mean_tipping_time
        log_mean_tipping_time = np.log(mean_tipping_time)

        # Linear regression fit of the logarithms
        line, lr_result = linear_regression_fit(log_distance_from_crit, log_mean_tipping_time)
        critical_exponent = -lr_result.slope

        # Plot fit
        fig, ax = linear_regression_plot(log_distance_from_crit, log_mean_tipping_time, fax=fax, param_values=False)
        ax.set_xlabel("$\log |S - S_{c}|$")
        ax.set_ylabel("$\log\\tau$")
        ax.set_title(
            f"{self.dissapearing_attractor.upper()} Critical Exponent Fit, $\\gamma = {critical_exponent:.2f}$"
        )
        ax.grid()
        return fig, ax

    def transient_lifetime_histogram(self, S, *args, grid_points=100, fax=None, **kwargs):
        "Uses kde to plot histogram of transient lifetimes"

        # Init fax
        if fax is None:
            fax = init_2d_fax()
        fig, ax = fax

        ds = self.observations(S_list=[S])["tipping_time"]

        # Plot Histogram
        ds.plot.hist(ax=ax, density=True)
        kde = gaussian_kde(ds.dropna())
        xs = np.linspace(0, ds.max() + ds.std(), grid_points)
        ax.plot(xs, kde(xs), *args, **kwargs)
        ax.set_xlabel("$\\tau_i$")
        ax.set_ylabel("$\\rho$")
        ax.set_title(f"S = {S:.2f}, Transient Lifetime Histogram")
        ax.grid()
        return fig, ax

    def all_transient_lifetime_histograms(self):
        for S in self.default_S_list:
            fig, ax = self.transient_lifetime_histogram(S)
            ax.set_title(f"S = {S:.2f}")
            fig.show()
        return
