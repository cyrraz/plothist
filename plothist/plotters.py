# -*- coding: utf-8 -*-
"""
Collection of functions to plot histograms
"""

import numpy as np
import matplotlib as mpl
import boost_histogram as bh
import matplotlib.pyplot as plt
import warnings
import re
from mpl_toolkits.axes_grid1 import make_axes_locatable


def create_comparison_figure(
    figsize=(6, 5),
    nrows=2,
    ncols=1,
    gridspec_kw={"height_ratios": [4, 1]},
    hspace=0.15,
):
    """
    Create a figure with subplots for comparison.

    Parameters
    ----------
    figsize : tuple, optional
        Figure size in inches. Default is (6, 5).
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
    if figsize is None:
        figsize = plt.rcParams["figure.figsize"]

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
            weights=np.nan_to_num(hist.values(), 0),
            **kwargs,
        )
    else:
        # Multiple histograms
        ax.hist(
            x=[h.axes[0].centers for h in hist],
            bins=hist[0].axes[0].edges,
            weights=[np.nan_to_num(h.values(), 0) for h in hist],
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
    if "edgecolors" not in pcolormesh_kwargs.keys():
        pcolormesh_kwargs["edgecolors"] = "face"
    im = ax.pcolormesh(*hist.axes.edges.T, hist.values().T, **pcolormesh_kwargs)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    ax.tick_params(axis="x", which="both", top=False, bottom=False)
    ax.get_figure().colorbar(im, cax=cax, **colorbar_kwargs)


def plot_error_hist(hist, ax, **kwargs):
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
    kwargs.setdefault("yerr", np.sqrt(hist.variances()))
    kwargs.setdefault("fmt", ".")

    ax.errorbar(
        x=hist.axes[0].centers,
        y=hist.values(),
        **kwargs,
    )


def compare_two_hist(
    hist_1,
    hist_2,
    xlabel=None,
    ylabel=None,
    h1_label="h1",
    h2_label="h2",
    save_as=None,
    fig=None,
    ax_main=None,
    ax_comparison=None,
    **comparison_kwargs,
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
    h1_label : str, optional
        The label for the first histogram. Default is "h1".
    h2_label : str, optional
        The label for the second histogram. Default is "h2".
    save_as : str or None, optional
        The path to save the figure. Default is None.
    fig : matplotlib.figure.Figure or None, optional
        The figure to use for the plot. If fig, ax_main and ax_comparison are None, a new figure will be created. Default is None.
    ax_main : matplotlib.axes.Axes or None, optional
        The main axes for the histogram comparison. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    ax_comparison : matplotlib.axes.Axes or None, optional
        The axes for the comparison plot. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    **comparison_kwargs : optional
        Arguments to be passed to plot_comparison(), including the choice of the comparison function and the treatment of the uncertainties (see documentation of plot_comparison() for details).

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
    if fig is None and ax_main is None and ax_comparison is None:
        fig, (ax_main, ax_comparison) = create_comparison_figure()
    elif fig is None or ax_main is None or ax_comparison is None:
        raise ValueError(
            "Need to provid fig, ax_main and ax_comparison (or None of them)."
        )

    if not np.all(hist_1.axes[0].edges == hist_2.axes[0].edges):
        raise ValueError("The bins of the compared histograms must be equal.")

    xlim = (hist_1.axes[0].edges[0], hist_1.axes[0].edges[-1])

    plot_hist(hist_1, ax=ax_main, label=h1_label, histtype="step")
    plot_hist(hist_2, ax=ax_main, label=h2_label, histtype="step")
    ax_main.set_xlim(xlim)
    ax_main.set_ylabel(ylabel)
    ax_main.tick_params(axis="x", labelbottom="off")
    ax_main.legend()
    _ = ax_main.xaxis.set_ticklabels([])

    plot_comparison(
        hist_1,
        hist_2,
        ax_comparison,
        xlabel=xlabel,
        h1_label=h1_label,
        h2_label=h2_label,
        **comparison_kwargs,
    )

    fig.align_ylabels()

    if save_as is not None:
        fig.savefig(save_as, bbox_inches="tight")

    return fig, ax_main, ax_comparison


def _hist_ratio_variances(hist_1, hist_2):
    """
    Calculate the variances of the ratio of two histograms (hist_1/hist_2).

    Parameters
    ----------
    hist_1 : boost_histogram.Histogram
        The first histogram.
    hist_2 : boost_histogram.Histogram
        The second histogram.

    Returns
    -------
    variances : np.ndarray
        The variances of the ratio of the two histograms.

    Raises
    ------
    ValueError
        If the bins of the histograms are not equal.
    """
    if not np.all(hist_1.axes[0].edges == hist_2.axes[0].edges):
        raise ValueError("The bins of the histograms must be equal.")

    np.seterr(divide="ignore", invalid="ignore")
    ratio_variances = np.where(
        hist_2.values() != 0,
        hist_1.variances() / hist_2.values() ** 2
        + hist_2.variances() * hist_1.values() ** 2 / hist_2.values() ** 4,
        np.nan,
    )
    np.seterr(divide="warn", invalid="warn")

    return ratio_variances


def plot_comparison(
    hist_1,
    hist_2,
    ax,
    xlabel="x1",
    h1_label="h1",
    h2_label="h2",
    comparison="ratio",
    comparison_ylabel=None,
    comparison_ylim=None,
    ratio_uncertainty="uncorrelated",
    **plot_hist_kwargs,
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
    h1_label : str, optional
        The label for the first histogram. Default is "h1".
    h2_label : str, optional
        The label for the second histogram. Default is "h2".
    comparison : str, optional
        The type of comparison to plot ("ratio", "pull" or "difference"). Default is "ratio".
    comparison_ylabel : str, optional
        The label for the y-axis. Default is h1_label/h2_label if comparison="ratio", and the pull formula used if "pull" .
    comparison_ylim : tuple or None, optional
        The y-axis limits for the comparison plot. Default is None. If None, standard y-axis limits are setup.
    ratio_uncertainty : str, optional
        How to treat the uncertainties of the histograms when comparison = "ratio" ("uncorrelated" for simple comparison, "split" for scaling and split hist_1 and hist_2 uncertainties). This argument has no effect if comparison != "ratio". Default is "uncorrelated".
    **plot_hist_kwargs : optional
        Arguments to be passed to plot_hist() or plot_error_hist(), called in case the comparison is "pull" or "ratio", respectively. In case of pull, the default arguments are histtype="stepfilled" and color="darkgrey". In case of ratio, the default argument is color="black".

    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes with the plotted comparison.

    See Also
    --------
    compare_two_hist : Compare two histograms and plot the comparison.

    """

    h1_label = get_math_text(h1_label)
    h2_label = get_math_text(h2_label)

    if not np.all(hist_1.axes[0].edges == hist_2.axes[0].edges):
        raise ValueError("The bins of the compared histograms must be equal.")

    np.seterr(divide="ignore", invalid="ignore")
    if comparison == "ratio":
        comparison_values = np.where(
            hist_2.values() != 0, hist_1.values() / hist_2.values(), np.nan
        )
        if ratio_uncertainty == "split":
            h1_scaled_uncertainties = np.where(
                hist_2.values() != 0,
                np.sqrt(hist_1.variances()) / hist_2.values(),
                np.nan,
            )
            h2_scaled_uncertainties = np.where(
                hist_2.values() != 0,
                np.sqrt(hist_2.variances()) / hist_2.values(),
                np.nan,
            )
            comparison_variances = h1_scaled_uncertainties ** 2
        elif ratio_uncertainty == "uncorrelated":
            comparison_variances = _hist_ratio_variances(hist_1, hist_2)
        else:
            raise ValueError("ratio_uncertainty not in ['uncorrelated', 'split'].")
    elif comparison == "pull":
        comparison_values = np.where(
            hist_1.variances() + hist_2.variances() != 0,
            (hist_1.values() - hist_2.values())
            / np.sqrt(hist_1.variances() + hist_2.variances()),
            np.nan,
        )
        comparison_variances = np.ones_like(comparison_values)
    elif comparison == "difference":
        comparison_values = hist_1.values() - hist_2.values()
        comparison_variances = hist_1.variances() + hist_2.variances()
    else:
        raise ValueError(
            f"{comparison} not available as a comparison ('ratio', 'pull' or 'difference')."
        )
    np.seterr(divide="warn", invalid="warn")

    hist_comparison = bh.Histogram(hist_2.axes[0], storage=bh.storage.Weight())
    hist_comparison[:] = np.stack([comparison_values, comparison_variances], axis=-1)

    if comparison == "pull":
        plot_hist_kwargs.setdefault("histtype", "stepfilled")
        plot_hist_kwargs.setdefault("color", "darkgrey")
        plot_hist(hist_comparison, ax=ax, **plot_hist_kwargs)
    else:
        plot_hist_kwargs.setdefault("color", "black")
        plot_error_hist(hist_comparison, ax=ax, **plot_hist_kwargs)

    if comparison == "ratio":
        if comparison_ylim is None:
            comparison_ylim = (0.0, 2.0)

        if ratio_uncertainty == "split":
            ax.bar(
                x=hist_2.axes[0].centers,
                bottom=np.nan_to_num(
                    1 - h2_scaled_uncertainties, nan=comparison_ylim[0]
                ),
                height=np.nan_to_num(
                    2 * h2_scaled_uncertainties, nan=2 * comparison_ylim[-1]
                ),
                width=hist_2.axes[0].widths,
                edgecolor="dimgrey",
                hatch="////",
                fill=False,
                lw=0,
            )
        ax.axhline(1, ls="--", lw=1.0, color="black")
        ax.set_ylabel(r"$\frac{" + h1_label + "}{" + h2_label + "}$")

    elif comparison == "pull":
        if comparison_ylim is None:
            comparison_ylim = (-5.0, 5.0)
        ax.axhline(0, ls="--", lw=1.0, color="black")
        ax.set_ylabel(
            rf"$\frac{{ {h1_label} - {h2_label} }}{{ \sqrt{{\sigma^2_{{{h1_label}}} + \sigma^2_{{{h2_label}}}}} }} $"
        )

    elif comparison == "difference":
        ax.axhline(0, ls="--", lw=1.0, color="black")
        ax.set_ylabel(f"${h1_label} - {h2_label}$")

    xlim = (hist_1.axes[0].edges[0], hist_1.axes[0].edges[-1])
    ax.set_xlim(xlim)
    if comparison_ylim is not None:
        ax.set_ylim(comparison_ylim)
    ax.set_xlabel(xlabel)
    if comparison_ylabel is not None:
        ax.set_ylabel(comparison_ylabel)

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


def get_math_text(text):
    match = re.search(r"\$(.*?)\$", text)
    if match:
        return match.group(1)
    else:
        return text
