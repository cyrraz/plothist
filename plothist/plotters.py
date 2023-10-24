# -*- coding: utf-8 -*-
"""
Collection of functions to plot histograms
"""

import numpy as np
import boost_histogram as bh
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
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
        Height spacing between subplots. Default is 0.15.

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

    for ax in axes[:-1]:
        _ = ax.xaxis.set_ticklabels([])

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


def plot_2d_hist(
    hist, fig=None, ax=None, ax_colorbar=None, pcolormesh_kwargs={}, colorbar_kwargs={}
):
    """
    Plot a 2D histogram using a pcolormesh plot and add a colorbar.

    Parameters
    ----------
    hist : boost_histogram.Histogram
        The 2D histogram to plot.
    fig : matplotlib.figure.Figure, optional
        The Figure instance for plotting. If fig, ax and ax_colorbar are None, a new figure will be created. Default is None.
    ax : matplotlib.axes.Axes, optional
        The Axes instance for plotting. If fig, ax and ax_colorbar are None, a new figure will be created. Default is None.
    ax_colorbar : matplotlib.axes.Axes
        The Axes instance for the colorbar. If fig, ax and ax_colorbar are None, a new figure will be created. Default is None.
    pcolormesh_kwargs : dict, optional
        Additional keyword arguments forwarded to ax.pcolormesh() (default is {}).
    colorbar_kwargs : dict, optional
        Additional keyword arguments forwarded to ax.get_figure().colorbar() (default is {}).
    """
    pcolormesh_kwargs.setdefault("edgecolors", "face")

    if fig is None and ax is None and ax_colorbar is None:
        fig, (ax, ax_colorbar) = plt.subplots(
            figsize=(5, 4.2), ncols=2, gridspec_kw={"width_ratios": [4, 0.3]}
        )
    elif fig is None or ax is None or ax_colorbar is None:
        raise ValueError("Need to provid fig, ax and ax_colorbar (or None of them).")

    im = ax.pcolormesh(*hist.axes.edges.T, hist.values().T, **pcolormesh_kwargs)
    ax.get_figure().colorbar(im, cax=ax_colorbar, **colorbar_kwargs)

    return fig, ax, ax_colorbar


def plot_2d_hist_with_projections(
    hist,
    xlabel=None,
    ylabel=None,
    ylabel_x_projection=None,
    xlabel_y_projection=None,
    colorbar_label=None,
    offset_x_labels=False,
    save_as=None,
    pcolormesh_kwargs={},
    colorbar_kwargs={},
    plot_hist_kwargs={},
):
    """Plot a 2D histogram with projections on the x and y axes.

    Parameters
    ----------
    hist : 2D boost_histogram.Histogram
        The 2D histogram to plot.
    xlabel : str, optional
        Label for the x axis. Default is None.
    ylabel : str, optional
        Label for the y axis. Default is None.
    ylabel_x_projection : str, optional
        Label for the y axis of the x projection. Default is None.
    xlabel_y_projection : str, optional
        Label for the x axis of the y projection. Default is None.
    colorbar_label : str, optional
        Label for the colorbar. Default is None.
    offset_x_labels : bool, optional
        Whether to offset the x labels to avoid overlapping with the exponent label (i.e. "10^X") of the axis. Default is False.
    save_as : str, optional
        Path to save the figure to. Default is None.
    pcolormesh_kwargs : dict, optional
        Keyword arguments for the pcolormesh call. Default is {}.
    colorbar_kwargs : dict, optional
        Keyword arguments for the colorbar call. Default is {}.
    plot_hist_kwargs : dict, optional
        Keyword arguments for the plot_hist call (x and y projections). Default is {}.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure.
    ax_2d : matplotlib.axes.Axes
        The axes for the 2D histogram.
    ax_x_projection : matplotlib.axes.Axes
        The axes for the x projection.
    ax_y_projection : matplotlib.axes.Axes
        The axes for the y projection.
    ax_colorbar : matplotlib.axes.Axes
        The axes for the colorbar.
    """

    colorbar_kwargs.setdefault("label", colorbar_label)
    plot_hist_kwargs.setdefault("histtype", "stepfilled")

    fig_width = 6
    fig_height = 6
    gridspec = [6, 0.72, 1.0]

    fig, axs = plt.subplots(
        figsize=(fig_width, fig_height),
        ncols=3,
        nrows=3,
        gridspec_kw={"width_ratios": gridspec, "height_ratios": gridspec[::-1]},
    )

    for x in range(3):
        for y in range(3):
            if not (x == 2 and y == 0):
                axs[x, y].remove()

    gs = axs[0, 0].get_gridspec()

    ax_2d = axs[2, 0]
    ax_x_projection = fig.add_subplot(gs[0:2, 0:1])
    ax_y_projection = fig.add_subplot(gs[-1, 1:])
    ax_colorbar = fig.add_subplot(gs[0:2, 1])

    plot_2d_hist(
        hist,
        fig=fig,
        ax=ax_2d,
        ax_colorbar=ax_colorbar,
        pcolormesh_kwargs=pcolormesh_kwargs,
        colorbar_kwargs=colorbar_kwargs,
    )
    plot_hist(hist[:, :: bh.sum], ax=ax_x_projection, **plot_hist_kwargs)
    plot_hist(
        hist[:: bh.sum, :],
        ax=ax_y_projection,
        orientation="horizontal",
        **plot_hist_kwargs,
    )

    _ = ax_x_projection.xaxis.set_ticklabels([])
    _ = ax_y_projection.yaxis.set_ticklabels([])

    xlim = (hist.axes[0].edges[0], hist.axes[0].edges[-1])
    ylim = (hist.axes[1].edges[0], hist.axes[1].edges[-1])
    ax_2d.set_xlim(xlim)
    ax_x_projection.set_xlim(xlim)
    ax_2d.set_ylim(ylim)
    ax_y_projection.set_ylim(ylim)

    if offset_x_labels:
        labelpad = 20
    else:
        labelpad = None

    ax_2d.set_xlabel(xlabel, labelpad=labelpad)
    ax_2d.set_ylabel(ylabel)
    ax_x_projection.set_ylabel(ylabel_x_projection)
    ax_y_projection.set_xlabel(xlabel_y_projection, labelpad=labelpad)

    hspace = 0.25
    wspace = 0.25
    fig.subplots_adjust(hspace=hspace, wspace=wspace)

    fig.align_ylabels()

    if save_as is not None:
        fig.savefig(save_as, bbox_inches="tight")

    return fig, ax_2d, ax_x_projection, ax_y_projection, ax_colorbar


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
        The type of comparison to plot ("ratio", "pull", "difference" or "relative_difference"). Default is "ratio".
    comparison_ylabel : str, optional
        The label for the y-axis. Default is the explicit formula used to compute the comparison plot.
    comparison_ylim : tuple or None, optional
        The y-axis limits for the comparison plot. Default is None. If None, standard y-axis limits are setup.
    ratio_uncertainty : str, optional
        How to treat the uncertainties of the histograms when comparison is "ratio" or "relative_difference" ("uncorrelated" for simple comparison, "split" for scaling and split hist_1 and hist_2 uncertainties). This argument has no effect if comparison != "ratio" or "relative_difference". Default is "uncorrelated".
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

    h1_label = _get_math_text(h1_label)
    h2_label = _get_math_text(h2_label)

    if not np.all(hist_1.axes[0].edges == hist_2.axes[0].edges):
        raise ValueError("The bins of the compared histograms must be equal.")

    np.seterr(divide="ignore", invalid="ignore")

    if comparison in ["ratio", "relative_difference"]:
        if comparison == "ratio":
            comparison_values = np.where(
                hist_2.values() != 0, hist_1.values() / hist_2.values(), np.nan
            )
        else:
            comparison_values = np.where(
                hist_2.values() != 0, (hist_1.values() / hist_2.values()) - 1, np.nan
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
            f"{comparison} not available as a comparison ('ratio', 'pull', 'difference' or 'relative_difference')."
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

    if comparison in ["ratio", "relative_difference"]:
        if comparison_ylim is None:
            if comparison == "relative_difference":
                comparison_ylim = (-1.0, 1.0)
            else:
                comparison_ylim = (0.0, 2.0)

        if comparison == "relative_difference":
            bottom_shift = 0
            ax.axhline(0, ls="--", lw=1.0, color="black")
            ax.set_ylabel(
                r"$\frac{" + h1_label + " - " + h2_label + "}{" + h2_label + "}$"
            )
        else:
            bottom_shift = 1
            ax.axhline(1, ls="--", lw=1.0, color="black")
            ax.set_ylabel(r"$\frac{" + h1_label + "}{" + h2_label + "}$")

        if ratio_uncertainty == "split":
            ax.bar(
                x=hist_2.axes[0].centers,
                bottom=np.nan_to_num(
                    bottom_shift - h2_scaled_uncertainties, nan=comparison_ylim[0]
                ),
                height=np.nan_to_num(
                    2 * h2_scaled_uncertainties,
                    nan=comparison_ylim[-1] - comparison_ylim[0],
                ),
                width=hist_2.axes[0].widths,
                edgecolor="dimgrey",
                hatch="////",
                fill=False,
                lw=0,
            )

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


def savefig(fig, path, new_figsize=None, adjust_after_tight_layout=False):
    """
    Save a Matplotlib figure with consistent figsize, axes size and subplot spacing.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The Matplotlib figure to be saved.

    path : str
        The output file path where the figure will be saved.

    new_figsize : tuple, optional
        The new figsize as a (width, height) tuple. If None, the original figsize is preserved.

    Returns
    -------
    None
    """
    old_width, old_height = fig.get_size_inches()

    if new_figsize is not None:
        width_scale = new_figsize[0] / old_width
        height_scale = new_figsize[1] / old_height
    else:
        width_scale = 1.0
        height_scale = 1.0

    axes = fig.get_axes()
    axes_dimensions = [
        (pos.width / width_scale, pos.height / height_scale)
        for pos in [ax.get_position() for ax in axes]
    ]
    wspace, hspace = fig.subplotpars.wspace, fig.subplotpars.hspace

    fig.tight_layout()
    fig.subplots_adjust(wspace=wspace, hspace=hspace)

    for k_ax, ax in enumerate(axes):
        ax.set_position(
            Bbox.from_bounds(
                ax.get_position().x0,
                ax.get_position().y0,
                axes_dimensions[k_ax][0],
                axes_dimensions[k_ax][1],
            )
        )
    if adjust_after_tight_layout:
        fig.subplots_adjust(wspace=wspace, hspace=hspace)

    fig.set_size_inches(old_width * width_scale, old_height * height_scale)

    fig.savefig(path)


def _get_math_text(text):
    match = re.search(r"\$(.*?)\$", text)
    if match:
        return match.group(1)
    else:
        return text
