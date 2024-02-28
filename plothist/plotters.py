# -*- coding: utf-8 -*-
"""
Collection of functions to plot histograms
"""

import numpy as np
import boost_histogram as bh
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import re
from plothist.comparison import (
    get_comparison,
    get_asymmetrical_uncertainties,
    _check_binning_consistency,
    _check_uncertainty_type,
)
from plothist.histogramming import _make_hist_from_function
from plothist.plothist_style import set_fitting_ylabel_fontsize


def create_comparison_figure(
    figsize=(6, 5),
    nrows=2,
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

    fig, axes = plt.subplots(nrows=nrows, figsize=figsize, gridspec_kw=gridspec_kw)
    if nrows > 1:
        fig.subplots_adjust(hspace=hspace)

    for ax in axes[:-1]:
        _ = ax.xaxis.set_ticklabels([])

    return fig, axes


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
        Additional keyword arguments forwarded to ax.hist(), such as density, color, label, histtype...
    """
    if not isinstance(hist, list):
        # Single histogram
        # Create a dummy data sample x made of the bin centers of the input histogram
        # Each dummy data point is weighed according to the bin content
        ax.hist(
            x=hist.axes[0].centers,
            bins=hist.axes[0].edges,
            weights=np.nan_to_num(hist.values(), 0),
            **kwargs,
        )
    else:
        # Multiple histograms
        _check_binning_consistency(hist)
        ax.hist(
            x=[h.axes[0].centers for h in hist],
            bins=hist[0].axes[0].edges,
            weights=[np.nan_to_num(h.values(), 0) for h in hist],
            **kwargs,
        )


def plot_2d_hist(
    hist,
    fig=None,
    ax=None,
    ax_colorbar=None,
    pcolormesh_kwargs={},
    colorbar_kwargs={},
    square_ax=True,
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
    square_ax : bool, optional
        Whether to make the main ax square (default is True).
    """
    # Create copies of the kwargs arguments passed as lists/dicts to avoid modifying them
    pcolormesh_kwargs = pcolormesh_kwargs.copy()
    colorbar_kwargs = colorbar_kwargs.copy()

    pcolormesh_kwargs.setdefault("edgecolors", "face")

    if fig is None and ax is None and ax_colorbar is None:
        fig, (ax, ax_colorbar) = plt.subplots(
            figsize=(6, 4.5), ncols=2, gridspec_kw={"width_ratios": [4, 0.23]}
        )
    elif fig is None or ax is None or ax_colorbar is None:
        raise ValueError("Need to provide fig, ax and ax_colorbar (or None of them).")

    if square_ax:
        ax.set_box_aspect(1)
        fig.subplots_adjust(wspace=0, hspace=0)

    im = ax.pcolormesh(*hist.axes.edges.T, hist.values().T, **pcolormesh_kwargs)
    ax.get_figure().colorbar(im, cax=ax_colorbar, **colorbar_kwargs)

    return fig, ax, ax_colorbar


def _invert_collection_order(ax, n=0):
    """
    Invert the order of the collection objects in an Axes instance.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Axes instance for plotting.
    n : int, optional
        The number of collections to keep in the original order. Default is 0.

    """
    # Retrieve the list of collection objects
    collections = list(ax.collections)

    # Separate the first n collections and reverse the rest
    first_n = collections[:n]
    rest = collections[n:]
    rest.reverse()

    # Remove all collections and re-add them in the new order
    for collection in ax.collections:
        collection.remove()
    for collection in first_n + rest:
        ax.add_collection(collection)


def plot_function(func, range, ax, stacked=False, npoints=1000, **kwargs):
    """
    Plot a 1D function on a given range.

    Parameters
    ----------
    func : function or list of functions
        The 1D function or list of functions to plot.
        The function(s) should support vectorization (i.e. accept a numpy array as input).
    range : tuple
        The range of the function(s). The function(s) will be plotted on the interval [range[0], range[1]].
    ax : matplotlib.axes.Axes
        The Axes instance for plotting.
    stacked : bool, optional
        Whether to use ax.stackplot() to plot the function(s) as a stacked plot. Default is False.
    npoints : int, optional
        The number of points to use for plotting. Default is 1000.
    **kwargs
        Additional keyword arguments forwarded to ax.plot() (in case stacked=False) or ax.stackplot() (in case stacked=True).
    """
    x = np.linspace(range[0], range[1], npoints)

    if not stacked:
        if not isinstance(func, list):
            ax.plot(x, func(x), **kwargs)
        else:
            ax.plot(
                x,
                np.array([func(x) for func in func]).T,
                **kwargs,
            )
    else:
        if kwargs.get("labels", None) is None:
            kwargs["labels"] = []

        if not isinstance(func, list):
            func = [func]
        n_collections_before = len(list(ax.collections))
        ax.stackplot(
            x,
            [f(x) for f in func],
            **kwargs,
        )
        # Invert the order of the collection objects to match the top-down order of the stackplot
        _invert_collection_order(ax, n_collections_before)


def plot_2d_hist_with_projections(
    hist,
    xlabel=None,
    ylabel=None,
    ylabel_x_projection=None,
    xlabel_y_projection=None,
    colorbar_label=None,
    offset_x_labels=False,
    pcolormesh_kwargs={},
    colorbar_kwargs={},
    plot_hist_kwargs={},
    figsize=(6, 6),
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
    pcolormesh_kwargs : dict, optional
        Keyword arguments for the pcolormesh call. Default is {}.
    colorbar_kwargs : dict, optional
        Keyword arguments for the colorbar call. Default is {}.
    plot_hist_kwargs : dict, optional
        Keyword arguments for the plot_hist call (x and y projections). Default is {}.
    figsize : tuple, optional
        Figure size in inches. Default is (6, 6). To get square bins if the figure is not square shaped, be sure to set the bins and the ranges of the histogram according to the ratio of the figure width and height.

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
    # Create copies of the kwargs arguments passed as lists/dicts to avoid modifying them
    pcolormesh_kwargs = pcolormesh_kwargs.copy()
    colorbar_kwargs = colorbar_kwargs.copy()
    plot_hist_kwargs = plot_hist_kwargs.copy()

    colorbar_kwargs.setdefault("label", colorbar_label)
    plot_hist_kwargs.setdefault("histtype", "stepfilled")

    gridspec_w = [figsize[0], 0.75, 1.5]
    gridspec_h = [1.5, 0.75, figsize[1]]

    fig, axs = plt.subplots(
        figsize=figsize,
        ncols=3,
        nrows=3,
        gridspec_kw={"width_ratios": gridspec_w, "height_ratios": gridspec_h},
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
        square_ax=False,
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

    return fig, ax_2d, ax_x_projection, ax_y_projection, ax_colorbar


def plot_error_hist(hist, ax, uncertainty_type="symmetrical", density=False, **kwargs):
    """
    Create an errorbar plot from a boost histogram.

    Parameters
    ----------
    hist : boost_histogram.Histogram
        The histogram to plot.
    ax : matplotlib.axes.Axes
        The Axes instance for plotting.
    uncertainty_type : str, optional
        What kind of bin uncertainty to use for hist: "symmetrical" for the Poisson standard deviation derived from the variance stored in the histogram object, "asymmetrical" for asymmetrical uncertainties based on a Poisson confidence interval. Default is "symmetrical".
        Asymmetrical uncertainties can only be computed for an unweighted histogram, because the bin contents of a weighted histogram do not follow a Poisson distribution.
        More information in :ref:`documentation-statistics-label`.
        The uncertainties are overwritten if the keyword argument yerr is provided.
    density : bool, optional
        Whether to normalize the histogram to unit area. Default is False.
    **kwargs
        Additional keyword arguments forwarded to ax.errorbar().
    """
    _check_uncertainty_type(uncertainty_type)

    if density:
        hist = hist.copy()
        hist *= 1 / (hist.values() * hist.axes[0].widths).sum()

    if uncertainty_type == "symmetrical":
        kwargs.setdefault("yerr", np.sqrt(hist.variances()))
    else:
        uncertainties_low, uncertainties_high = get_asymmetrical_uncertainties(hist)
        kwargs.setdefault("yerr", [uncertainties_low, uncertainties_high])

    kwargs.setdefault("fmt", ".")

    ax.errorbar(
        x=hist.axes[0].centers,
        y=hist.values(),
        **kwargs,
    )


def plot_hist_uncertainties(hist, ax, **kwargs):
    """
    Plot the symmetrical uncertainty of a histogram, the Poisson standard deviation derived from the variance stored in the histogram, as a hatched area.

    Parameters
    ----------
    hist : boost_histogram.Histogram
        The histogram from which we want to plot the uncertainties.
    ax : matplotlib.axes.Axes
        The Axes instance for plotting.
    **kwargs
        Additional keyword arguments forwarded to ax.bar().
    """
    uncertainty = np.sqrt(hist.variances())

    kwargs.setdefault("edgecolor", "dimgrey")
    kwargs.setdefault("hatch", "////")
    kwargs.setdefault("fill", False)
    kwargs.setdefault("lw", 0)

    ax.bar(
        x=hist.axes[0].centers,
        bottom=hist.values() - uncertainty,
        height=2 * uncertainty,
        width=hist.axes[0].widths,
        **kwargs,
    )


def plot_two_hist_comparison(
    h1,
    h2,
    xlabel=None,
    ylabel=None,
    h1_label="h1",
    h2_label="h2",
    fig=None,
    ax_main=None,
    ax_comparison=None,
    **comparison_kwargs,
):
    """
    Compare two histograms.

    Parameters
    ----------
    h1 : boost_histogram.Histogram
        The first histogram to compare.
    h2 : boost_histogram.Histogram
        The second histogram to compare.
    xlabel : str, optional
        The label for the x-axis. Default is None.
    ylabel : str, optional
        The label for the y-axis. Default is None.
    h1_label : str, optional
        The label for the first histogram. Default is "h1".
    h2_label : str, optional
        The label for the second histogram. Default is "h2".
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

    _check_binning_consistency([h1, h2])

    if fig is None and ax_main is None and ax_comparison is None:
        fig, (ax_main, ax_comparison) = create_comparison_figure()
    elif fig is None or ax_main is None or ax_comparison is None:
        raise ValueError(
            "Need to provide fig, ax_main and ax_comparison (or none of them)."
        )

    xlim = (h1.axes[0].edges[0], h1.axes[0].edges[-1])

    plot_hist(h1, ax=ax_main, label=h1_label, histtype="step")
    plot_hist(h2, ax=ax_main, label=h2_label, histtype="step")
    ax_main.set_xlim(xlim)
    ax_main.set_ylabel(ylabel)
    ax_main.legend()
    _ = ax_main.xaxis.set_ticklabels([])

    plot_comparison(
        h1,
        h2,
        ax_comparison,
        xlabel=xlabel,
        h1_label=h1_label,
        h2_label=h2_label,
        **comparison_kwargs,
    )

    fig.align_ylabels()

    return fig, ax_main, ax_comparison


def plot_comparison(
    h1,
    h2,
    ax,
    xlabel="",
    h1_label="h1",
    h2_label="h2",
    comparison="ratio",
    comparison_ylabel=None,
    comparison_ylim=None,
    h1_uncertainty_type="symmetrical",
    ratio_uncertainty_type="uncorrelated",
    **plot_hist_kwargs,
):
    """
    Plot the comparison between two histograms.

    Parameters
    ----------
    h1 : boost_histogram.Histogram
        The first histogram for comparison.
    h2 : boost_histogram.Histogram
        The second histogram for comparison.
    ax : matplotlib.axes.Axes
        The axes to plot the comparison.
    xlabel : str, optional
        The label for the x-axis. Default is "".
    h1_label : str, optional
        The label for the first histogram. Default is "h1".
    h2_label : str, optional
        The label for the second histogram. Default is "h2".
    comparison : str, optional
        The type of comparison to plot ("ratio", "pull", "difference", "relative_difference", "efficiency", or "asymmetry"). Default is "ratio".
    comparison_ylabel : str, optional
        The label for the y-axis. Default is the explicit formula used to compute the comparison plot.
    comparison_ylim : tuple or None, optional
        The y-axis limits for the comparison plot. Default is None. If None, standard y-axis limits are setup.
    h1_uncertainty_type : str, optional
        What kind of bin uncertainty to use for h1: "symmetrical" for the Poisson standard deviation derived from the variance stored in the histogram object, "asymmetrical" for asymmetrical uncertainties based on a Poisson confidence interval. Default is "symmetrical".
        Asymmetrical uncertainties are not supported for the asymmetry and efficiency comparisons.
    ratio_uncertainty_type : str, optional
        How to treat the uncertainties of the histograms when comparison is "ratio" or "relative_difference":
        This argument has no effect if comparison != "ratio" or "relative_difference".
        The options are:
        * "uncorrelated" for the comparison of two uncorrelated histograms,
        * "split" for scaling the uncertainties of h1 by the inverse of the bin content of h2, i.e. assuming zero uncertainty coming from h2 in the ratio uncertainty, and plotting separately scaled h2 uncertainties.
        Default is "uncorrelated".
    **plot_hist_kwargs : optional
        Arguments to be passed to plot_hist(), called in case the comparison is "pull", or plot_error_hist(), called for every other comparison case. In the former case, the default arguments are histtype="stepfilled" and color="darkgrey". In the later case, the default argument is color="black".

    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes with the plotted comparison.

    See Also
    --------
    plot_two_hist_comparison : Compare two histograms and plot the comparison.

    """

    h1_label = _get_math_text(h1_label)
    h2_label = _get_math_text(h2_label)

    _check_binning_consistency([h1, h2])

    comparison_values, lower_uncertainties, upper_uncertainties = get_comparison(
        h1, h2, comparison, h1_uncertainty_type, ratio_uncertainty_type
    )

    if np.allclose(lower_uncertainties, upper_uncertainties, equal_nan=True):
        hist_comparison = bh.Histogram(h2.axes[0], storage=bh.storage.Weight())
        hist_comparison[:] = np.c_[comparison_values, lower_uncertainties**2]
    else:
        plot_hist_kwargs.setdefault("yerr", [lower_uncertainties, upper_uncertainties])
        hist_comparison = bh.Histogram(h2.axes[0], storage=bh.storage.Weight())
        hist_comparison[:] = np.c_[comparison_values, np.zeros_like(comparison_values)]

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

        if ratio_uncertainty_type == "split":
            np.seterr(divide="ignore", invalid="ignore")
            h2_scaled_uncertainties = np.where(
                h2.values() != 0,
                np.sqrt(h2.variances()) / h2.values(),
                np.nan,
            )
            np.seterr(divide="warn", invalid="warn")
            ax.bar(
                x=h2.axes[0].centers,
                bottom=np.nan_to_num(
                    bottom_shift - h2_scaled_uncertainties, nan=comparison_ylim[0]
                ),
                height=np.nan_to_num(
                    2 * h2_scaled_uncertainties,
                    nan=comparison_ylim[-1] - comparison_ylim[0],
                ),
                width=h2.axes[0].widths,
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

    elif comparison == "efficiency":
        if comparison_ylim is None:
            comparison_ylim = (0.0, 1.0)
        ax.set_ylabel("Efficiency")

    elif comparison == "asymmetry":
        if comparison_ylim is None:
            comparison_ylim = (-1.0, 1.0)
        ax.axhline(0, ls="--", lw=1.0, color="black")
        ax.set_ylabel(rf"$\frac{{{h1_label} - {h2_label}}}{{{h1_label} + {h2_label}}}$")

    xlim = (h1.axes[0].edges[0], h1.axes[0].edges[-1])
    ax.set_xlim(xlim)
    ax.set_xlabel(xlabel)
    if comparison_ylim is not None:
        ax.set_ylim(comparison_ylim)
    if comparison_ylabel is not None:
        ax.set_ylabel(comparison_ylabel)

    return ax


def savefig(fig, path, new_figsize=None):
    """
    Save a Matplotlib figure with consistent figsize, axes size and subplot spacing (experimental feature).

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

    fig.set_size_inches(old_width * width_scale, old_height * height_scale)

    fig.savefig(path)


def _get_math_text(text):
    """
    Search for text between $ and return it.

    Parameters
    ----------
    text : str
        The input string.

    Returns
    -------
    str
        The text between $ or the input string if no $ are found.
    """
    match = re.search(r"\$(.*?)\$", text)
    if match:
        return match.group(1)
    else:
        return text


def _get_model_type(components):
    """
    Check that all components of a model are either all histograms or all functions
    and return the type of the model components.

    Parameters
    ----------
    components : list
        The list of model components.

    Returns
    -------
    str
        The type of the model components ("histograms" or "functions").

    Raises
    ------
    ValueError
        If the model components are not all histograms or all functions.
    """
    if all(isinstance(x, bh.Histogram) for x in components):
        return "histograms"
    elif all(callable(x) for x in components):
        return "functions"
    else:
        raise ValueError("All model components must be either histograms or functions.")


def plot_model(
    stacked_components=[],
    stacked_labels=None,
    stacked_colors=None,
    unstacked_components=[],
    unstacked_labels=None,
    unstacked_colors=None,
    xlabel=None,
    ylabel=None,
    stacked_kwargs={},
    unstacked_kwargs_list=[],
    model_sum_kwargs={"show": True, "label": "Model", "color": "navy"},
    function_range=None,
    model_uncertainty=True,
    model_uncertainty_label="Model stat. unc.",
    fig=None,
    ax=None,
):
    """
    Plot model made of a collection of histograms.

    Parameters
    ----------
    stacked_components : list of boost_histogram.Histogram, optional
        The list of histograms to be stacked composing the model. Default is [].
    stacked_labels : list of str, optional
        The labels of the model stacked components. Default is None.
    stacked_colors : list of str, optional
        The colors of the model stacked components. Default is None.
    unstacked_components : list of boost_histogram.Histogram, optional
        The list of histograms not to be stacked composing the model. Default is [].
    unstacked_labels : list of str, optional
        The labels of the model unstacked components. Default is None.
    unstacked_colors : list of str, optional
        The colors of the model unstacked components. Default is None.
    xlabel : str, optional
        The label for the x-axis. Default is None.
    ylabel : str, optional
        The label for the y-axis. Default is None.
    stacked_kwargs : dict, optional
        The keyword arguments used when plotting the stacked components in plot_hist() or plot_function(), one of which is called only once. Default is {}.
    unstacked_kwargs_list : list of dict, optional
        The list of keyword arguments used when plotting the unstacked components in plot_hist() or plot_function(), one of which is called once for each unstacked component. Default is [].
    model_sum_kwargs : dict, optional
        The keyword arguments for the plot_hist() function for the sum of the model components.
        Has no effect if all the model components are stacked.
        The special keyword "show" can be used with a boolean to specify whether to show or not the sum of the model components.
        Default is {"show": True, "label": "Model", "color": "navy"}.
    function_range : tuple, optional (mandatory if the model is made of functions)
        The range for the x-axis if the model is made of functions.
    model_uncertainty : bool, optional
        If False, set the model uncertainties to zeros. Default is True.
    model_uncertainty_label : str, optional
        The label for the model uncertainties. Default is "Model stat. unc.".
    fig : matplotlib.figure.Figure or None, optional
        The Figure object to use for the plot. Create a new one if none is provided.
    ax : matplotlib.axes.Axes or None, optional
        The Axes object to use for the plot. Create a new one if none is provided.


    Returns
    -------
    fig : matplotlib.figure.Figure
        The Figure object containing the plot.
    ax : matplotlib.axes.Axes
        The Axes object containing the plot.

    """

    # Create copies of the kwargs arguments passed as lists/dicts to avoid modifying them
    stacked_kwargs = stacked_kwargs.copy()
    unstacked_kwargs_list = unstacked_kwargs_list.copy()
    model_sum_kwargs = model_sum_kwargs.copy()

    components = stacked_components + unstacked_components

    if len(components) == 0:
        raise ValueError("Need to provide at least one model component.")

    model_type = _get_model_type(components)

    if model_type == "histograms":
        _check_binning_consistency(components)

    if fig is None and ax is None:
        fig, ax = plt.subplots()
    elif fig is None or ax is None:
        raise ValueError("Need to provide both fig and ax (or none).")

    if model_type == "histograms":
        xlim = (components[0].axes[0].edges[0], components[0].axes[0].edges[-1])
    else:
        if function_range is None:
            raise ValueError(
                "Need to provide function_range for model made of functions."
            )
        xlim = function_range

    if len(stacked_components) > 0:
        # Plot the stacked components
        stacked_kwargs.setdefault("edgecolor", "black")
        stacked_kwargs.setdefault("linewidth", 0.5)
        if model_type == "histograms":
            stacked_kwargs.setdefault("histtype", "stepfilled")
            plot_hist(
                stacked_components,
                ax=ax,
                stacked=True,
                color=stacked_colors,
                label=stacked_labels,
                **stacked_kwargs,
            )
            if model_uncertainty and len(unstacked_components) == 0:
                plot_hist_uncertainties(
                    sum(stacked_components), ax=ax, label=model_uncertainty_label
                )
        else:
            plot_function(
                stacked_components,
                ax=ax,
                stacked=True,
                colors=stacked_colors,
                labels=stacked_labels,
                range=xlim,
                **stacked_kwargs,
            )

    if len(unstacked_components) > 0:
        # Plot the unstacked components
        if unstacked_colors is None:
            unstacked_colors = [None] * len(unstacked_components)
        if unstacked_labels is None:
            unstacked_labels = [None] * len(unstacked_components)
        if len(unstacked_kwargs_list) == 0:
            unstacked_kwargs_list = [{}] * len(unstacked_components)
        for component, color, label, unstacked_kwargs in zip(
            unstacked_components,
            unstacked_colors,
            unstacked_labels,
            unstacked_kwargs_list,
        ):
            if model_type == "histograms":
                unstacked_kwargs.setdefault("histtype", "step")
                plot_hist(
                    component,
                    ax=ax,
                    stacked=False,
                    color=color,
                    label=label,
                    **unstacked_kwargs,
                )
            else:
                plot_function(
                    component,
                    ax=ax,
                    stacked=False,
                    color=color,
                    label=label,
                    range=xlim,
                    **unstacked_kwargs,
                )
        # Plot the sum of all the components
        if model_sum_kwargs.pop("show", True) and (
            len(unstacked_components) > 1 or len(stacked_components) > 0
        ):
            if model_type == "histograms":
                plot_hist(
                    sum(components),
                    ax=ax,
                    histtype="step",
                    **model_sum_kwargs,
                )
                if model_uncertainty:
                    plot_hist_uncertainties(
                        sum(components), ax=ax, label=model_uncertainty_label
                    )
            else:

                def sum_function(x):
                    return sum(f(x) for f in components)

                plot_function(
                    sum_function,
                    ax=ax,
                    range=xlim,
                    **model_sum_kwargs,
                )
        elif (
            model_uncertainty
            and len(stacked_components) == 0
            and len(unstacked_components) == 1
            and model_type == "histograms"
        ):
            plot_hist_uncertainties(
                sum(components), ax=ax, label=model_uncertainty_label
            )

    ax.set_xlim(xlim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    set_fitting_ylabel_fontsize(ax)
    ax.legend()

    return fig, ax


def plot_data_model_comparison(
    data_hist,
    stacked_components=[],
    stacked_labels=None,
    stacked_colors=None,
    unstacked_components=[],
    unstacked_labels=None,
    unstacked_colors=None,
    xlabel=None,
    ylabel=None,
    data_label="Data",
    stacked_kwargs={},
    unstacked_kwargs_list=[],
    model_sum_kwargs={"show": True, "label": "Sum", "color": "navy"},
    model_uncertainty=True,
    model_uncertainty_label="Model stat. unc.",
    data_uncertainty_type="asymmetrical",
    fig=None,
    ax_main=None,
    ax_comparison=None,
    **comparison_kwargs,
):
    """
    Compare data to model. The data uncertainties are computed using the Poisson confidence interval.

    Parameters
    ----------
    data_hist : boost_histogram.Histogram
        The histogram for the data.
    stacked_components : list of boost_histogram.Histogram, optional
        The list of histograms to be stacked composing the model. Default is [].
    stacked_labels : list of str, optional
        The labels of the model stacked components. Default is None.
    stacked_colors : list of str, optional
        The colors of the model stacked components. Default is None.
    unstacked_components : list of boost_histogram.Histogram, optional
        The list of histograms not to be stacked composing the model. Default is [].
    unstacked_labels : list of str, optional
        The labels of the model unstacked components. Default is None.
    unstacked_colors : list of str, optional
        The colors of the model unstacked components. Default is None.
    xlabel : str, optional
        The label for the x-axis. Default is None.
    ylabel : str, optional
        The label for the y-axis. Default is None.
    data_label : str, optional
        The label for the data. Default is "Data".
    stacked_kwargs : dict, optional
        The keyword arguments used when plotting the stacked components in plot_hist() or plot_function(), one of which is called only once. Default is {}.
    unstacked_kwargs_list : list of dict, optional
        The list of keyword arguments used when plotting the unstacked components in plot_hist() or plot_function(), one of which is called once for each unstacked component. Default is [].
    model_sum_kwargs : dict, optional
        The keyword arguments for the plot_hist() function for the sum of the model components.
        Has no effect if all the model components are stacked.
        The special keyword "show" can be used with a boolean to specify whether to show or not the sum of the model components.
        Default is {"show": True, "label": "Sum", "color": "navy"}.
    model_uncertainty : bool, optional
        If False, set the model uncertainties to zeros. Default is True.
    model_uncertainty_label : str, optional
        The label for the model uncertainties. Default is "Model stat. unc.".
    data_uncertainty_type : str, optional
        What kind of bin uncertainty to use for data_hist: "symmetrical" for the Poisson standard deviation derived from the variance stored in the histogram object, "asymmetrical" for asymmetrical uncertainties based on a Poisson confidence interval. Default is "asymmetrical".
    fig : matplotlib.figure.Figure or None, optional
        The figure to use for the plot. If fig, ax_main and ax_comparison are None, a new figure will be created. Default is None.
    ax_main : matplotlib.axes.Axes or None, optional
        The main axes for the histogram comparison. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    ax_comparison : matplotlib.axes.Axes or None, optional
        The axes for the comparison plot. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    **comparison_kwargs : optional
        Arguments to be passed to plot_comparison(), including the choice of the comparison function and the treatment of the uncertainties (see documentation of plot_comparison() for details). If they are not provided explicitly, the following arguments are passed by default: h1_label="Data", h2_label="Pred.", comparison="ratio", and ratio_uncertainty_type="split".

    Returns
    -------
    fig : matplotlib.figure.Figure
        The Figure object containing the plots.
    ax_main : matplotlib.axes.Axes
        The Axes object for the main plot.
    ax_comparison : matplotlib.axes.Axes
        The Axes object for the comparison plot.

    See Also
    --------
    plot_comparison : Plot the comparison between two histograms.

    """
    comparison_kwargs.setdefault("h1_label", data_label)
    comparison_kwargs.setdefault("h2_label", "Pred.")
    comparison_kwargs.setdefault("comparison", "ratio")
    comparison_kwargs.setdefault("ratio_uncertainty_type", "split")

    model_components = stacked_components + unstacked_components

    if len(model_components) == 0:
        raise ValueError("Need to provide at least one model component.")

    model_type = _get_model_type(model_components)

    if model_type == "histograms":
        _check_binning_consistency(model_components + [data_hist])

    if fig is None and ax_main is None and ax_comparison is None:
        fig, (ax_main, ax_comparison) = create_comparison_figure()
    elif fig is None or ax_main is None or ax_comparison is None:
        raise ValueError(
            "Need to provide fig, ax_main and ax_comparison (or none of them)."
        )

    plot_model(
        stacked_components=stacked_components,
        stacked_labels=stacked_labels,
        stacked_colors=stacked_colors,
        unstacked_components=unstacked_components,
        unstacked_labels=unstacked_labels,
        unstacked_colors=unstacked_colors,
        ylabel=ylabel,
        stacked_kwargs=stacked_kwargs,
        unstacked_kwargs_list=unstacked_kwargs_list,
        model_sum_kwargs=model_sum_kwargs,
        function_range=[data_hist.axes[0].edges[0], data_hist.axes[0].edges[-1]],
        model_uncertainty=model_uncertainty,
        model_uncertainty_label=model_uncertainty_label,
        fig=fig,
        ax=ax_main,
    )

    plot_error_hist(
        data_hist,
        ax=ax_main,
        uncertainty_type=data_uncertainty_type,
        color="black",
        label=data_label,
    )

    _ = ax_main.xaxis.set_ticklabels([])

    if model_type == "histograms":
        model_hist = sum(model_components)
        if not model_uncertainty:
            model_hist[:] = np.c_[
                model_hist.values(), np.zeros_like(model_hist.values())
            ]
    else:
        model_hist = _make_hist_from_function(
            lambda x: sum(f(x) for f in model_components), data_hist
        )

    if comparison_kwargs["comparison"] == "pull" and (
        model_type == "functions" or not model_uncertainty
    ):
        comparison_kwargs.setdefault(
            "comparison_ylabel",
            rf"$\frac{{ {comparison_kwargs['h1_label']} - {comparison_kwargs['h2_label']} }}{{ \sigma_{{{comparison_kwargs['h1_label']}}} }} $",
        )

    ax_main.legend()

    plot_comparison(
        data_hist,
        model_hist,
        ax=ax_comparison,
        xlabel=xlabel,
        h1_uncertainty_type=data_uncertainty_type,
        **comparison_kwargs,
    )

    ylabel_fontsize = set_fitting_ylabel_fontsize(ax_main)
    ax_comparison.get_yaxis().get_label().set_size(ylabel_fontsize)

    fig.align_ylabels()

    return fig, ax_main, ax_comparison
