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


def create_comparison_figure(
    figsize=(6, 4),
    nrows=2,
    ncols=1,
    gridspec_kw={"height_ratios": [4, 1]},
    hspace=0.125,
):
    """
    Create a figure with subplots for comparison.

    Parameters
    ----------
    figsize : tuple, optional
        Figure size in inches. Default is (6, 4).
    nrows : int, optional
        Number of rows in the subplot grid. Default is 2.
    ncols : int, optional
        Number of columns in the subplot grid. Default is 1.
    gridspec_kw : dict, optional
        Additional keyword arguments for the GridSpec. Default is {"height_ratios": [4, 1]}.
    hspace : float, optional
        Height spacing between subplots. Default is 0.125.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created figure.
    axes : ndarray
        Array of Axes objects representing the subplots.

    """
    fig, axes = plt.subplots(
        nrows=nrows, ncols=ncols, figsize=figsize, gridspec_kw=gridspec_kw
    )
    if nrows > 1:
        fig.subplots_adjust(hspace=hspace)

    return fig, axes


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


def compare_two_hist(
    hist_1,
    hist_2,
    xlabel=None,
    ylabel=None,
    x1_label="x1",
    x2_label="x2",
    comparison="ratio",
    comparison_ylim=None,
    ratio_uncertainty="uncorrelated",
    save_as=None,
    fig=None,
    ax_main=None,
    ax_comparison=None,
):
    """
    Compare two histograms.

    Parameters
    ----------
    hist_1 : boost_histogram.Histogram
        The first histogram to compare.
    hist_2 : boost_histogram.Histogram
        The second histogram to compare.
    xlabel : str, optional
        The label for the x-axis. Default is None.
    ylabel : str, optional
        The label for the y-axis. Default is None.
    x1_label : str, optional
        The label for the first histogram. Default is "x1".
    x2_label : str, optional
        The label for the second histogram. Default is "x2".
    comparison : str, optional
        The type of comparison to plot. Default is "ratio".
    comparison_ylim : tuple or None, optional
        The y-axis limits for the comparison plot. Default is None.
    save_as : str or None, optional
        The path to save the figure. Default is None.
    fig : matplotlib.figure.Figure or None, optional
        The figure to use for the plot. If fig, ax_main and ax_comparison are None, a new figure will be created. Default is None.
    ax_main : matplotlib.axes.Axes or None, optional
        The main axes for the histogram comparison. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    ax_comparison : matplotlib.axes.Axes or None, optional
        The axes for the comparison plot. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    **kwargs
        Additional keyword arguments to be passed to the plot_comparison function.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created figure.
    ax_main : matplotlib.axes.Axes
        The main axes for the histogram comparison.
    ax_comparison : matplotlib.axes.Axes
        The axes for the comparison plot.

    See Also
    --------
    plot_comparison : Plot the comparison between two histograms.

    """
    if not np.all(hist_1.axes[0].edges == hist_2.axes[0].edges):
        raise ValueError("The bins of the compared histograms must be equal.")

    if fig is None and ax_main is None and ax_comparison is None:
        fig, (ax_main, ax_comparison) = create_comparison_figure()
    elif (fig is not None or ax_main is not None or ax_comparison is not None) and (
        fig is None or ax_main is None or ax_comparison is None
    ):
        raise ValueError(
            "Need to provid fig, ax_main and ax_comparison (or None of them)."
        )

    xlim = (hist_1.axes[0].edges[0], hist_1.axes[0].edges[-1])

    plot_hist(hist_1, ax=ax_main, label=x1_label, histtype="step")
    plot_hist(hist_2, ax=ax_main, label=x2_label, histtype="step")
    ax_main.set_xlim(xlim)
    ax_main.set_ylabel(ylabel)
    ax_main.tick_params(axis="x", labelbottom="off")
    ax_main.legend(framealpha=0.5)
    _ = ax_main.xaxis.set_ticklabels([])
    fig.subplots_adjust(hspace=0.125)

    plot_comparison(
        hist_1,
        hist_2,
        ax_comparison,
        xlabel=xlabel,
        x1_label=x1_label,
        x2_label=x2_label,
        comparison=comparison,
        comparison_ylim=comparison_ylim,
        ratio_uncertainty=ratio_uncertainty,
    )

    if save_as is not None:
        fig.savefig(save_as, bbox_inches="tight")

    return fig, ax_main, ax_comparison


def plot_comparison(
    hist_1,
    hist_2,
    ax,
    xlabel="x1",
    x1_label="x1",
    x2_label="x2",
    comparison="ratio",
    comparison_ylim=None,
    ratio_uncertainty="uncorrelated",
):
    """
    Plot the comparison between two histograms.

    Parameters
    ----------
    hist_1 : boost_histogram.Histogram
        The first histogram for comparison.
    hist_2 : boost_histogram.Histogram
        The second histogram for comparison.
    ax : matplotlib.axes.Axes
        The axes to plot the comparison.
    xlabel : str, optional
        The label for the x-axis. Default is "x1".
    x1_label : str, optional
        The label for the first histogram. Default is "x1".
    x2_label : str, optional
        The label for the second histogram. Default is "x2".
    comparison : str, optional
        The type of comparison to plot ("ratio" or "pull"). Default is "ratio".
    comparison_ylim : tuple or None, optional
        The y-axis limits for the comparison plot. Default is None.
    ratio_uncertainty : str, optional
        How to treat the uncertainties of the histograms when comparison = "ratio" ("uncorrelated" for simple comparison, "split" for scaling and split hist_1 and hist_2 uncertainties)

    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes with the plotted comparison.

    See Also
    --------
    compare_two_hist : Compare two histograms and plot the comparison.

    """
    if not np.all(hist_1.axes[0].edges == hist_2.axes[0].edges):
        raise ValueError("The bins of the compared histograms must be equal.")

    np.seterr(divide="ignore", invalid="ignore")
    if comparison == "ratio":
        ratio_values = np.where(
            hist_2.values() != 0, hist_1.values() / hist_2.values(), np.nan
        )
        if ratio_uncertainty == "split" :
            ratio_variance = (np.sqrt(hist_1.variances()) / hist_1.values()) ** 2
        elif ratio_uncertainty == "uncorrelated":
            ratio_variance = np.where(
                hist_2.values() != 0,
                hist_1.variances() / hist_2.values() ** 2
                + hist_2.variances() * hist_1.values() ** 2 / hist_2.values() ** 4,
                np.nan,
            )
        else:
            raise ValueError("ratio_uncertainty not in ['uncorrelated', 'split'].")
        if ratio_uncertainty == "split" :
            h2_uncertainty = np.sqrt(hist_2.variances()) / hist_2.values()

    elif comparison == "pull":
        ratio_values = np.where(
            hist_2.values() != 0,
            (hist_1.values() - hist_2.values())
            / np.sqrt(hist_1.variances() + hist_2.variances()),
            np.nan,
        )
        ratio_variance = np.where(
            hist_1.values() != 0,
            1,
            np.nan,
        )
    else:
        raise ValueError(
            f"{comparison} not available as a comparison (use ratio or pull)."
        )

    np.seterr(divide="warn", invalid="warn")

    ax.errorbar(
        x=hist_2.axes[0].centers,
        xerr=None,
        y=np.nan_to_num(ratio_values, nan=0),
        yerr=np.nan_to_num(np.sqrt(ratio_variance), nan=0),
        fmt=".",
        color="black",
    )

    if comparison == "ratio":
        if ratio_uncertainty == "split":
            ax.bar(
                x=hist_2.axes[0].centers,
                bottom=np.nan_to_num(1 - h2_uncertainty, nan=0),
                height=np.nan_to_num(2 * h2_uncertainty, nan=100),
                width=hist_2.axes[0].widths,
                edgecolor="dimgrey",
                hatch="////",
                fill=False,
                lw=0,
            )
        ax.axhline(1, ls="--", lw=1.0, color="black")
        ax.set_ylabel(r"$\frac{" + x1_label + "}{" + x2_label + "}$")
        if comparison_ylim is None:
            ax.set_ylim(0.0, 2.0)
        else:
            ax.set_ylim(comparison_ylim)

    elif comparison == "pull":
        ax.axhline(0, ls="--", lw=1.0, color="black")
        ax.set_ylabel(
            rf"$\frac{{ {x1_label} - {x2_label} }}{{ \sqrt{{\sigma^2_{{{x1_label}}} + \sigma^2_{{{x2_label}}}}} }} $"
        )
        if comparison_ylim is None:
            ax.set_ylim(-5.0, 5.0)
        else:
            ax.set_ylim(comparison_ylim)

    xlim = (hist_1.axes[0].edges[0], hist_1.axes[0].edges[-1])
    ax.set_xlim(xlim)
    ax.set_xlabel(xlabel)

    return ax


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
