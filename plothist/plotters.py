# -*- coding: utf-8 -*-
""" Collection of functions to plot histograms
"""

import numpy as np
import matplotlib as mpl
import boost_histogram as bh
import matplotlib.pyplot as plt
import warnings
from dataclasses import dataclass
import yaml
import os


def create_variable_registry(variables, path="./variable_registry.yaml", reset=False):
    """Create the variable registry yaml file given a list of variables
    It stores all the plotting information for each variable
    The user can then easily change the parameters in the yaml

    Plotting parameters:
        Key: Key of the variable in the yaml
        name: variable name in data
        bins
        range
        label: latex supported
        log: True if logscale
        legend_location
        legend_ncols
        docstring
    """

    if not os.path.exists(path):
        with open(path, "w") as f:
            pass

    with open(path, "r") as f:
        variable_registry = yaml.safe_load(f)
        if variable_registry is None:
            variable_registry = {}

        for variable in variables:
            if variable not in variable_registry.keys() or reset:
                variable_registry.update(
                    {
                        variable: {
                            "name": variable,
                            "bins": 50,
                            "range": ["min", "max"],
                            "label": variable,
                            "log": False,
                            "legend_location": "best",
                            "legend_ncols": 1,
                            "docstring": "",
                        }
                    }
                )

    with open(path, "w") as f:
        for key, value in variable_registry.items():
            yaml.safe_dump({key: value}, f, sort_keys=False)
            f.write("\n" * 2)


def get_variable_from_registry(variable, path="./variable_registry.yaml"):
    if not os.path.exists(path):
        if path == "./variable_registry.yaml":
            raise RuntimeError("Did you forgot to run create_variable_registry()?")

    with open(path, "r") as f:
        variable_registry = yaml.safe_load(f)
        return variable_registry[variable]


def update_variable_registry(
    variable_key, x_min, x_max, path="./variable_registry.yaml"
):
    # TODO: extend updating function
    if not os.path.exists(path):
        if path == "./variable_registry.yaml":
            raise RuntimeError("Did you forgot to run create_variable_registry()?")

    with open(path, "r") as f:
        variable_registry = yaml.safe_load(f)
    variable_registry[variable_key]["range"] = [x_min, x_max]

    with open(path, "w") as f:
        for key, value in variable_registry.items():
            yaml.safe_dump({key: value}, f, sort_keys=False)
            f.write("\n" * 2)


def update_variable_registry_ranges(data, variables, path="./variable_registry.yaml"):
    for variable_key in variables:
        variable = get_variable_from_registry(variable_key, path=path)
        binning = _format_binning(
            data[variable_key], variable["range"], variable["bins"]
        )
        update_variable_registry(variable_key, binning[1], binning[2], path=path)


def _format_binning(data, range, bins):
    # Inspired from np.histograms
    if range is not None:
        x_min = min(data) if range[0] == "min" else range[0]
        x_max = max(data) if range[1] == "max" else range[1]
        if x_min > x_max:
            raise ValueError("max must be larger than min in range parameter.")
        if not (np.isfinite(x_min) and np.isfinite(x_max)):
            raise ValueError(
                "supplied range of [{}, {}] is not finite".format(x_min, x_max)
            )
    elif data.size == 0:
        # handle empty arrays. Can't determine range, so use 0-1.
        x_min, x_max = 0, 1
    else:
        x_min, x_max = min(data), max(data)
        if not (np.isfinite(x_min) and np.isfinite(x_max)):
            raise ValueError(
                "autodetected range of [{}, {}] is not finite".format(x_min, x_max)
            )

    # expand empty range to avoid divide by zero
    if x_min == x_max:
        x_min = x_min - 0.5
        x_max = x_max + 0.5

    return (bins, x_min, x_max)


def _flatten_2d_hist(hist):
    # TODO: support other storages, generalise to N dimensions
    n_bins = hist.axes[0].size * hist.axes[1].size
    flatten_hist = bh.Histogram(
        bh.axis.Regular(n_bins, 0, n_bins), storage=bh.storage.Weight()
    )
    flatten_hist[:] = np.c_[hist.values().flatten(), hist.variances().flatten()]
    return flatten_hist


def make_hist(data, bins=50, range=None, weights=1):
    """Create a histogram object and fill it
    Parameters
    ----------
    data : 1D array-like
        Data used to fill a histogram.
    binning : (int, float, float), default: (50,None,None)
        Binning, with format (number of bins, lower bound, upper bound)
    weights : float or array-like, default=1
        A single weight to apply to all the data points, or an array-like to apply weights to each data point
    Returns
    -------
    histogram: boost_histogram.Histogram
        filled histogram
    """

    binning = _format_binning(data, range, bins)

    if weights is None:
        storage = bh.storage.Double()
    else:
        storage = bh.storage.Weight()

    h = bh.Histogram(bh.axis.Regular(*binning), storage=storage)
    h.fill(data, weight=weights, threads=0)

    # Check what proportion of the data is in the underflow and overflow bins
    range_coverage = h.values().sum() / h.values(flow=True).sum()
    # Issue a warning in more than 1% of the data is outside of the binning range
    if range_coverage < 0.99:
        warnings.warn(
            f"Only {100*range_coverage:.2f}% of data contained in the binning range ({binning[1]}, {binning[2]})."
        )

    return h


def make_2d_hist(data, binning, weights=1):
    """Create a 2D histogram object and fill it
    Parameters
    ----------
    data : DD array-like
        Data used to fill a histogram.
    binning : list((int, float, float))
        Binning, with format (number of bins, lower bound, upper bound)
    weights : float or array-like, default=1
        A single weight to apply to all the data points, or an array-like to apply weights to each data point
    Returns
    -------
    histogram: boost_histogram.Histogram
        filled histogram
    """

    if weights is None:
        storage = bh.storage.Double()
    else:
        storage = bh.storage.Weight()

    h = bh.Histogram(
        bh.axis.Variable(binning[0]), bh.axis.Variable(binning[1]), storage=storage
    )
    h.fill(*data, weight=weights, threads=0)

    # Check what proportion of the data is in the underflow and overflow bins
    range_coverage = h.values().sum() / h.values(flow=True).sum()
    # Issue a warning in more than 1% of the data is outside of the binning range
    if range_coverage < 0.99:
        warnings.warn(
            f"Only {100*range_coverage:.2f}% of data contained in the binning range."
        )

    return h


def plot_hist(hist, ax, **kwargs):
    """Histogram plot from boost histogram.
    Parameters
    ----------
    hist : boost_histogram.Histogram
        Histogram or list of histograms to plot.
    ax : matplotlib.axes.Axes
        Axes instance for plotting.
    **kwargs
        Keyword arguments forwarded to ax.hist().
    Returns
    -------
    None
    """
    if not isinstance(hist, list):
        # Single histogram
        # A data sample x made of the bin centers of the input histogram
        # Each "data point" is weighed according to the bin content
        ax.hist(
            x=hist.axes[0].centers,
            bins=hist.axes[0].edges,
            weights=hist.values(),
            **kwargs,
        )
    else:
        # Multiple histograms
        ax.hist(
            x=[h.axes[0].centers for h in hist],
            bins=hist[0].axes[0].edges,
            weights=[h.values() for h in hist],
            **kwargs,
        )


def plot_error_hist(hist, ax, **kwargs):
    """Errorbar plot from boost histogram.
    Parameters
    ----------
    hist : boost_histogram.Histogram
        Histogram to plot.
    ax : matplotlib.axes.Axes
        Axes instance for plotting.
    **kwargs
        Keyword arguments forwarded to ax.errorbar().
    Returns
    -------
    None
    """
    # TODO: Allow the user to provide xerr, yerr, fmt themselves.
    ax.errorbar(
        x=hist.axes[0].centers,
        xerr=None,
        y=hist.values(),
        yerr=np.sqrt(hist.variances()),
        fmt=".",
        **kwargs,
    )


def plot_hist_difference(hist1, hist2, ax, **kwargs):
    """Plot histogram difference.
    Parameters
    ----------
    hist1, hist2 : boost_histogram.Histogram
        Histogram for difference hist1-hist2.
    ax : matplotlib.axes.Axes
        Axes instance for plotting.
    **kwargs
        Keyword arguments forwarded to ax.errorbar().
    Returns
    -------
    None
    """
    difference = hist1.values() - hist2.values()
    difference_uncertainty = np.sqrt(hist1.variances() + hist2.variances())
    ax.errorbar(
        x=hist1.axes[0].centers,
        xerr=None,
        y=difference,
        yerr=difference_uncertainty,
        fmt=".",
        **kwargs,
    )


def compare_two_hist(
    hist_1, hist_2, xlabel=None, ylabel=None, x1_label="x1", x2_label="x2", save_as=None
):
    """Compare two histograms
    Returns
    -------
    fig, ax_comparison, ax_ratio

    """

    if not np.all(hist_1.axes[0].edges == hist_2.axes[0].edges):
        raise ValueError("The bins of the compared histograms must be equal.")

    fig, (ax_comparison, ax_ratio) = plt.subplots(
        2, gridspec_kw={"height_ratios": [4, 1]}
    )

    xlim = (hist_1.axes[0].edges[0], hist_1.axes[0].edges[-1])

    plot_hist(hist_1, ax=ax_comparison, label=x1_label, histtype="step")
    plot_hist(hist_2, ax=ax_comparison, label=x2_label, histtype="step")
    ax_comparison.set_xlim(xlim)
    ax_comparison.set_ylabel(ylabel)
    ax_comparison.tick_params(axis="x", labelbottom="off")
    ax_comparison.legend(framealpha=0.5)

    np.seterr(divide="ignore", invalid="ignore")
    ratio = np.where(hist_1.values() != 0, hist_2.values() / hist_1.values(), np.nan)
    ratio_variance = np.where(
        hist_1.values() != 0,
        hist_2.variances() / hist_1.values() ** 2
        + hist_1.variances() * hist_2.values() ** 2 / hist_1.values() ** 4,
        np.nan,
    )
    np.seterr(divide="warn", invalid="warn")

    ax_ratio.errorbar(
        x=hist_1.axes[0].centers,
        xerr=None,
        y=np.nan_to_num(ratio, nan=0),
        yerr=np.nan_to_num(np.sqrt(ratio_variance), nan=0),
        fmt=".",
        color="dimgrey",
    )

    ax_ratio.axhline(1, ls="--", lw=1.0, color="black")
    ax_ratio.set_ylim(0.0, 1.5)
    ax_ratio.set_xlim(xlim)
    ax_ratio.set_xlabel(xlabel)
    ax_ratio.set_ylabel(r"$\frac{" + x2_label + "}{" + x1_label + "}$", fontsize=18)

    _ = ax_comparison.xaxis.set_ticklabels([])

    if save_as is not None:
        fig.savefig(save_as, bbox_inches="tight")

    return fig, ax_comparison, ax_ratio


def cubehelix_palette(
    ncolors=7,
    start=1.5,
    rotation=1.5,
    gamma=1.0,
    hue=0.8,
    lightest=0.8,
    darkest=0.3,
    reverse=True,
):
    """
    Make a sequential palette from the cubehelix system, in which the perceived brightness is linearly increasing.
    This code is adapted from seaborn, which implements equation (2) of reference [1] below.

    Parameters
    ----------
    ncolors : int
        Number of colors in the palette.
    start : float, 0 <= start <= 3
        Direction of the predominant colour deviation from black
        at the start of the colour scheme (1=red, 2=green, 3=blue).
    rotation : float
        Number of rotations around the hue wheel over the range of the palette.
    gamma : float 0 <= gamma
        Gamma factor to emphasize darker (gamma < 1) or lighter (gamma > 1)
        colors.
    hue : float, 0 <= hue <= 1
        Saturation of the colors.
    darkest : float 0 <= dark <= 1
        Intensity of the darkest color in the palette.
    lightest : float 0 <= light <= 1
        Intensity of the lightest color in the palette.
    reverse : bool
        If True, the palette will go from dark to light.

    Returns
    -------
    list of RGB tuples

    References
    ----------
    [1] Green, D. A. (2011). "A colour scheme for the display of astronomical
    intensity images". Bulletin of the Astromical Society of India, Vol. 39,
    p. 289-295.
    """

    def f(x0, x1):
        # Adapted from matplotlib
        def color(lambda_):
            # emphasise either low intensity values (gamma < 1),
            # or high intensity values (γ > 1)
            lambda_gamma = lambda_**gamma

            # Angle and amplitude for the deviation
            # from the black to white diagonal
            # in the plane of constant perceived intensity
            a = hue * lambda_gamma * (1 - lambda_gamma) / 2

            phi = 2 * np.pi * (start / 3 + rotation * lambda_)

            return lambda_gamma + a * (x0 * np.cos(phi) + x1 * np.sin(phi))

        return color

    cdict = {
        "red": f(-0.14861, 1.78277),
        "green": f(-0.29227, -0.90649),
        "blue": f(1.97294, 0.0),
    }

    cmap = mpl.colors.LinearSegmentedColormap("cubehelix", cdict)

    x = np.linspace(lightest, darkest, int(ncolors))
    pal = cmap(x)[:, :3].tolist()
    if reverse:
        pal = pal[::-1]
    return pal


@dataclass
class Variable:
    """Simple structure containing information about how a variable is binned and plotted."""

    name: str
    binning: tuple
