# -*- coding: utf-8 -*-
"""
Collection of functions to plot histograms
"""

import numpy as np
import matplotlib as mpl
import boost_histogram as bh
import matplotlib.pyplot as plt
import warnings
from mpl_toolkits.axes_grid1 import make_axes_locatable
from dataclasses import dataclass
import yaml
import os


def create_variable_registry(variables, path="./variable_registry.yaml", reset=False):
    # TODO: bins can be a list for 2D uneven binning
    """Create the variable registry yaml file given a list of variables.
    It stores all the plotting information for each variable.

    It checks if the variable registry file exists. If not, it creates an empty file at the specified path.
    It then loads the existing variable registry, or creates an empty registry if it doesn't exist.
    For each variable in the input list, if the variable is not already in the registry or the reset flag is True,
    it adds the variable to the registry with default settings.
    Finally, it writes the updated variable registry back to the file.

    Parameters of one variable in the yaml:

    name : str
        variable name in data.
    bins : int
        Number of bins, default is 50.
    range: list of two float
        Range of the variables, default is [min, max] of the data.
    label : str
        Label to display, default is variable name. Latex supported by surrounding the label with $label$.
    log : bool
        True if plot in logscale, default is False
    legend_location : str
        Default is best
    legend_ncols : int
        Default set to 1
    docstring : str
        Default is empty

    Parameters
    ----------
    variables : list
        A list of variable names to be registered.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").
    reset : bool, optional
        If True, the registry will be reset for all variables (default is False).


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
    """
    This function retrieves the parameter information for a variable from the variable registry file specified by the 'path' parameter.
    It loads the variable registry file and returns the dictionary entry corresponding to the specified variable name.

    Parameters
    ----------
    variable : str
        The name of the variable for which to retrieve parameter information.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").

    Returns
    -------
    dict
        A dictionary containing the parameter information for the specified variable.

    See also
    --------
    create_variable_registry
    """

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
    """
    Update the range parameter for a variable in the variable registry file.

    Parameters
    ----------
    variable_key : str
        The key identifier of the variable to update in the registry.
    x_min : float
        The new minimum value for the range of the variable.
    x_max : float
        The new maximum value for the range of the variable.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").

    Returns
    -------
    None

    See Also
    --------
    create_variable_registry
    """
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
    """
    Update the range parameters for multiple variables in the variable registry file.

    Parameters
    ----------
    data : dict
        A dictionary containing the data for the variables.
    variables : list
        A list of variable keys for which to update the range parameters in the registry.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").

    Returns
    -------
    None

    Raises
    ------
    NotImplementedError
        If non-regular binning is encountered in the registry.

    See Also
    --------
    get_variable_from_registry, update_variable_registry, create_axis

    """
    for variable_key in variables:
        variable = get_variable_from_registry(variable_key, path=path)
        axis = create_axis(data[variable_key], variable["bins"], variable["range"])
        if isinstance(axis, bh.axis.Regular):
            update_variable_registry(
                variable_key, float(axis.edges[0]), float(axis.edges[-1]), path=path
            )
        else:
            raise NotImplemented(
                f"Only regular binning allowed in registry. {type(axis)}"
            )


def create_axis(data, bins, range):
    """
    Create an axis object for histogram binning based on the input data and parameters.

    Parameters
    ----------
    data : array-like
        The input data for determining the axis range.
    bins : int or array-like
        The number of bins or bin edges for the axis.
    range : None or tuple, optional
        The range of the axis. If None, it will be determined based on the data.

    Returns
    -------
    Axis object
        An axis object for histogram binning.

    Raises
    ------
    ValueError
        If the range parameter is invalid or not finite.
    """

    try:
        N = len(bins)
    except TypeError:
        N = 1

    if N > 1:
        if range is not None:
            warnings.warn(f"Custom binning -> ignore supplied range ({range}).")
        return bh.axis.Variable(bins)

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

    return bh.axis.Regular(bins, x_min, x_max)


def _flatten_2d_hist(hist):
    # TODO: support other storages, generalise to N dimensions
    """
    Flatten a 2D histogram into a 1D histogram.

    Parameters
    ----------
    hist : Histogram object
        The 2D histogram to be flattened.

    Returns
    -------
    Histogram object
        The flattened 1D histogram.
    """
    n_bins = hist.axes[0].size * hist.axes[1].size
    flatten_hist = bh.Histogram(
        bh.axis.Regular(n_bins, 0, n_bins), storage=bh.storage.Weight()
    )
    flatten_hist[:] = np.c_[hist.values().flatten(), hist.variances().flatten()]
    return flatten_hist


def make_hist(data, bins=50, range=None, weights=1):
    """
    Create a histogram object and fill it with the provided data.

    Parameters
    ----------
    data : array-like
        1D array-like data used to fill the histogram.
    bins : int or tuple, optional
        Binning specification for the histogram (default is 50).
        If an integer, it represents the number of bins.
        If a tuple, it should be the explicit list of all bin edges.
    range : tuple, optional
        The range of values to consider for the histogram bins (default is None).
        If None, the range is determined from the data.
    weights : float or array-like, optional
        Weight(s) to apply to the data points (default is 1).
        If a float, a single weight is applied to all data points.
        If an array-like, weights are applied element-wise.

    Returns
    -------
    histogram : boost_histogram.Histogram
        The filled histogram object.
    """

    axis = create_axis(data, bins, range)

    if weights is None:
        storage = bh.storage.Double()
    else:
        storage = bh.storage.Weight()

    h = bh.Histogram(axis, storage=storage)
    h.fill(data, weight=weights, threads=0)

    # Check what proportion of the data is in the underflow and overflow bins
    range_coverage = h.values().sum() / h.values(flow=True).sum()
    # Issue a warning in more than 1% of the data is outside of the binning range
    if range_coverage < 0.99:
        warnings.warn(
            f"Only {100*range_coverage:.2f}% of data contained in the binning range ({axis.edges[0]}, {axis.edges[-1]})."
        )

    return h


def make_2d_hist(data, bins=(10, 10), range=(None, None), weights=1):
    """
    Create a 2D histogram object and fill it with the provided data.

    Parameters
    ----------
    data : array-like
        2D array-like data used to fill the histogram.
    bins : tuple, optional
        Binning specification for each dimension of the histogram (default is (10, 10)).
        Each element of the tuple represents the number of bins for the corresponding dimension.
        Also support explicit bin edges specification (for non-constant bin size).
    range : tuple, optional
        The range of values to consider for each dimension of the histogram (default is (None, None)).
        If None, the range is determined from the data for that dimension.
        The tuple should have the same length as the data.
    weights : float or array-like, optional
        Weight(s) to apply to the data points (default is 1).
        If a float, a single weight is applied to all data points.
        If an array-like, weights are applied element-wise.

    Returns
    -------
    histogram : boost_histogram.Histogram
        The filled 2D histogram object.

    Raises
    ------
    ValueError
        If the data does not have two components or if the lengths of x and y are not equal.
    """
    if len(data) != 2:
        raise ValueError("data should have two components, x and y")
    if len(data[0]) != len(data[1]):
        raise ValueError("x and y must have the same length.")

    if weights is None:
        storage = bh.storage.Double()
    else:
        storage = bh.storage.Weight()

    h = bh.Histogram(
        create_axis(data[0], bins[0], range[0]),
        create_axis(data[1], bins[1], range[1]),
        storage=storage,
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
    """
    Plot a histogram or a list of histograms from boost_histogram.

    Parameters
    ----------
    hist : boost_histogram.Histogram or list of boost_histogram.Histogram
        The histogram(s) to plot.
    ax : matplotlib.axes.Axes
        The Axes instance for plotting.
    **kwargs
        Additional keyword arguments forwarded to ax.hist().
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


def plot_2d_hist(hist, ax, pcolormesh_kwargs={}, colorbar_kwargs={}):
    """
    Plot a 2D histogram using a pcolormesh plot and add a colorbar.

    Parameters
    ----------
    hist : boost_histogram.Histogram
        The 2D histogram to plot.
    ax : matplotlib.axes.Axes
        The Axes instance for plotting.
    pcolormesh_kwargs : dict, optional
        Additional keyword arguments forwarded to ax.pcolormesh() (default is {}).
    colorbar_kwargs : dict, optional
        Additional keyword arguments forwarded to ax.get_figure().colorbar() (default is {}).
    """
    im = ax.pcolormesh(*hist.axes.edges.T, hist.values().T, **pcolormesh_kwargs)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    ax.tick_params(axis="x", which="both", top=False, bottom=False)
    ax.get_figure().colorbar(im, cax=cax, **colorbar_kwargs)


def plot_error_hist(hist, ax, **kwargs):
    # TODO: Allow the user to provide xerr, yerr, fmt themselves.
    """
    Create an errorbar plot from a boost histogram.

    Parameters
    ----------
    hist : boost_histogram.Histogram
        The histogram to plot.
    ax : matplotlib.axes.Axes
        The Axes instance for plotting.
    **kwargs
        Additional keyword arguments forwarded to ax.errorbar().
    """
    ax.errorbar(
        x=hist.axes[0].centers,
        xerr=None,
        y=hist.values(),
        yerr=np.sqrt(hist.variances()),
        fmt=".",
        **kwargs,
    )


def plot_hist_difference(hist1, hist2, ax, **kwargs):
    """
    Plot the difference between two histograms.

    Parameters
    ----------
    hist1, hist2 : boost_histogram.Histogram
        The histograms for which the difference hist1 - hist2 will be plotted.
    ax : matplotlib.axes.Axes
        The Axes instance for plotting.
    **kwargs
        Additional keyword arguments forwarded to ax.errorbar().
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
    hist_1,
    hist_2,
    xlabel=None,
    ylabel=None,
    x1_label="x1",
    x2_label="x2",
    comparison="ratio",
    ylim_comparison=None,
    save_as=None,
):
    """
    Compare two histograms.

    Parameters
    ----------
    hist_1, hist_2 : boost_histogram.Histogram
        The histograms to be compared.
    xlabel : str, optional
        The label for the x-axis of the comparison plot.
    ylabel : str, optional
        The label for the y-axis of the comparison plot.
    x1_label, x2_label : str, optional
        The labels for the two histograms being compared.
    comparison: str, optional
        How to compare the two histograms.
        Available comparisons: 'ratio' to compute the difference and 'pull' to compute the pulls between the two histograms
    ylim_comparison: list of float, optional
        Set the ylim of the ax_comparison. If not specified, ylim = [0., 2.] for ratio comparison and [-5., 5.] for pull.
    save_as : str, optional
        If provided, the filename to save the figure as.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The generated figure.
    ax_main : matplotlib.axes.Axes
        The axes for the histogram comparison plot.
    ax_comparison : matplotlib.axes.Axes
        The axes for the comparison plot.

    """
    if not np.all(hist_1.axes[0].edges == hist_2.axes[0].edges):
        raise ValueError("The bins of the compared histograms must be equal.")

    fig, (ax_main, ax_comparison) = plt.subplots(
        2, gridspec_kw={"height_ratios": [4, 1]}
    )

    xlim = (hist_1.axes[0].edges[0], hist_1.axes[0].edges[-1])

    plot_hist(hist_1, ax=ax_main, label=x1_label, histtype="step")
    plot_hist(hist_2, ax=ax_main, label=x2_label, histtype="step")
    ax_main.set_xlim(xlim)
    ax_main.set_ylabel(ylabel)
    ax_main.tick_params(axis="x", labelbottom="off")
    ax_main.legend(framealpha=0.5)

    np.seterr(divide="ignore", invalid="ignore")
    if comparison == "ratio":
        ratio_values = np.where(
            hist_1.values() != 0, hist_2.values() / hist_1.values(), np.nan
        )
        ratio_variance = np.where(
            hist_1.values() != 0,
            hist_2.variances() / hist_1.values() ** 2
            + hist_1.variances() * hist_2.values() ** 2 / hist_1.values() ** 4,
            np.nan,
        )
    elif comparison == "pull":
        ratio_values = np.where(
            hist_1.values() != 0,
            (hist_2.values() - hist_1.values())
            / np.sqrt(hist_1.variances() + hist_2.variances()),
            np.nan,
        )
        ratio_variance = np.where(
            hist_1.values() != 0,
            1,
            np.nan,
        )
    else:
        raise ValueError(f"{comparison} not available as a comparison (use ratio or pull).")

    np.seterr(divide="warn", invalid="warn")

    ax_comparison.errorbar(
        x=hist_1.axes[0].centers,
        xerr=None,
        y=np.nan_to_num(ratio_values, nan=0),
        yerr=np.nan_to_num(np.sqrt(ratio_variance), nan=0),
        fmt=".",
        color="dimgrey",
    )

    if comparison == "ratio":
        ax_comparison.axhline(1, ls="--", lw=1.0, color="black")
        ax_comparison.set_ylabel(r"$\frac{" + x2_label + "}{" + x1_label + "}$")
        if ylim_comparison is None:
            ax_comparison.set_ylim(0.0, 2.0)
        else:
            ax_comparison.set_ylim(ylim_comparison)
    elif comparison == "pull":
        ax_comparison.axhline(0, ls="--", lw=1.0, color="black")
        ax_comparison.set_ylabel("Pulls")
        if ylim_comparison is None:
            ax_comparison.set_ylim(-5.0, 5.0)
        else:
            ax_comparison.set_ylim(ylim_comparison)
    ax_comparison.set_xlim(xlim)
    ax_comparison.set_xlabel(xlabel)

    _ = ax_main.xaxis.set_ticklabels([])

    if save_as is not None:
        fig.savefig(save_as, bbox_inches="tight")

    return fig, ax_main, ax_comparison


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
    ncolors : int, optional
        Number of colors in the palette.
    start : float, 0 <= start <= 3, optional
        Direction of the predominant colour deviation from black
        at the start of the colour scheme (1=red, 2=green, 3=blue).
    rotation : float, optional
        Number of rotations around the hue wheel over the range of the palette.
    gamma : float, 0 <= gamma, optional
        Gamma factor to emphasize darker (gamma < 1) or lighter (gamma > 1)
        colors.
    hue : float, 0 <= hue <= 1, optional
        Saturation of the colors.
    darkest : float, 0 <= darkest <= 1, optional
        Intensity of the darkest color in the palette.
    lightest : float, 0 <= lightest <= 1, optional
        Intensity of the lightest color in the palette.
    reverse : bool, optional
        If True, the palette will go from dark to light.

    Returns
    -------
    list of RGB tuples
        The generated palette of colors represented as a list of RGB tuples.


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
            lambda_gamma = lambda_ ** gamma

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
