"""
Collection of functions to plot histograms in the context of High Energy Physics
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from plothist.plotters import (
    plot_hist,
    plot_error_hist,
    _flatten_2d_hist,
    compare_two_hist,
    plot_comparison,
    create_comparison_figure,
)


def compare_data_mc(
    data_hist,
    mc_hist_list,
    signal_hist=None,
    xlabel=None,
    ylabel=None,
    mc_labels=None,
    mc_colors=None,
    comparison="ratio",
    comparison_ylim=None,
    save_as=None,
    flatten_2d_hist=False,
    stacked=True,
    fig=None,
    ax_main=None,
    ax_comparison=None,
    ratio_uncertainty="split",
):
    """
    Compare data to MC simulations.

    Parameters
    ----------
    data_hist : boost_histogram.Histogram
        The histogram for the data.
    mc_hist_list : list of boost_histogram.Histogram
        The list of histograms for MC simulations.
    signal_hist : boost_histogram.Histogram, optional
        The histogram for the signal. Default is None.
    xlabel : str, optional
        The label for the x-axis. Default is None.
    ylabel : str, optional
        The label for the y-axis. Default is None.
    mc_labels : list of str, optional
        The labels for the MC simulations. Default is None.
    mc_colors : list of str, optional
        The colors for the MC simulations. Default is None.
    comparison : str, optional
        The type of comparison to plot ("ratio" or "pull"). Default is "ratio".
    comparison_ylim : tuple or None, optional
        The y-axis limits for the comparison axis. Default is (0, 2) for "ratio" and (-5, 5) for "pull".
    save_as : str or None, optional
        The file path to save the figure. Default is None.
    flatten_2d_hist : bool, optional
        If True, flatten 2D histograms to 1D before plotting. Default is False.
    stacked : bool, optional
        If True, stack the MC histograms. If False, plot them side by side. Default is True.
    fig : matplotlib.figure.Figure or None, optional
        The figure to use for the plot. If fig, ax_main and ax_comparison are None, a new figure will be created. Default is None.
    ax_main : matplotlib.axes.Axes or None, optional
        The main axes for the histogram comparison. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    ax_comparison : matplotlib.axes.Axes or None, optional
        The axes for the comparison plot. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    ratio_uncertainty : str, optional
        How to treat the uncertainties of the histograms when comparison = "ratio" ("uncorrelated" for simple comparison, "split" for scaling and split hist_1 and hist_2 uncertainties). Default is "split".

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
    plot_comparison : Plot the comparison between data and MC simulations.

    """

    if fig is None and ax_main is None and ax_comparison is None:
        fig, (ax_main, ax_comparison) = create_comparison_figure()
    elif fig is None or ax_main is None or ax_comparison is None:
        raise ValueError(
            "Need to provid fig, ax_main and ax_comparison (or None of them)."
        )

    if flatten_2d_hist:
        mc_hist_list = [_flatten_2d_hist(h) for h in mc_hist_list]
        data_hist = _flatten_2d_hist(data_hist)
        if signal_hist:
            signal_hist = _flatten_2d_hist(signal_hist)

    plot_mc(
        mc_hist_list,
        signal_hist=signal_hist,
        ylabel=ylabel,
        mc_labels=mc_labels,
        mc_colors=mc_colors,
        fig=fig,
        ax=ax_main,
        stacked=stacked,
        flatten_2d_hist=False,  # Already done
    )

    plot_error_hist(data_hist, ax=ax_main, color="black", label="Data")

    _ = ax_main.xaxis.set_ticklabels([])

    # Plot MC statistical uncertainty
    mc_hist_total = sum(mc_hist_list)
    mc_uncertainty = np.sqrt(mc_hist_total.variances())
    ax_main.bar(
        x=mc_hist_total.axes[0].centers,
        bottom=mc_hist_total.values() - mc_uncertainty,
        height=2 * mc_uncertainty,
        width=mc_hist_total.axes[0].widths,
        edgecolor="dimgrey",
        hatch="////",
        fill=False,
        lw=0,
        label="Stat. unc.",
    )

    ax_main.legend()

    plot_comparison(
        data_hist,
        mc_hist_total,
        ax=ax_comparison,
        xlabel=xlabel,
        x1_label="Data",
        x2_label="Pred.",
        comparison=comparison,
        comparison_ylim=comparison_ylim,
        ratio_uncertainty=ratio_uncertainty,
    )

    if save_as is not None:
        fig.savefig(save_as, bbox_inches="tight")

    return fig, ax_main, ax_comparison


def plot_mc(
    mc_hist_list,
    signal_hist=None,
    xlabel=None,
    ylabel=None,
    mc_labels=None,
    mc_colors=None,
    signal_label="Signal",
    fig=None,
    ax=None,
    save_as=None,
    flatten_2d_hist=False,
    stacked=True,
    leg_ncol=1,
):
    """
    Plot MC simulation histograms.

    Parameters
    ----------
    mc_hist_list : list of boost_histogram.Histogram
        The list of histograms for MC simulations.
    signal_hist : boost_histogram.Histogram, optional
        The histogram for the signal. Default is None.
    xlabel : str, optional
        The label for the x-axis. Default is None.
    ylabel : str, optional
        The label for the y-axis. Default is None.
    mc_labels : list of str, optional
        The labels for the MC simulations. Default is None.
    mc_colors : list of str, optional
        The colors for the MC simulations. Default is None.
    signal_label : str, optional
        The label for the signal. Default is "Signal".
    fig : matplotlib.figure.Figure or None, optional
        The Figure object to use for the plot. Create a new one if none is provided.
    ax : matplotlib.axes.Axes or None, optional
        The Axes object to use for the plot. Create a new one if none is provided.
    save_as : str or None, optional
        The file path to save the figure. Default is None.
    flatten_2d_hist : bool, optional
        If True, flatten 2D histograms to 1D before plotting. Default is False.
    stacked : bool, optional
        If True, stack the MC histograms. If False, plot them side by side. Default is True.
    leg_ncol : int, optional
        The number of columns for the legend. Default is 1.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The Figure object containing the plot.
    ax : matplotlib.axes.Axes
        The Axes object containing the plot.

    """

    if fig is None and ax is None:
        fig, ax = plt.subplots()
    elif fig is None or ax is None:
        raise ValueError("Need to provid both fig and ax (or None).")

    if flatten_2d_hist:
        mc_hist_list = [_flatten_2d_hist(h) for h in mc_hist_list]
        if signal_hist:
            signal_hist = _flatten_2d_hist(signal_hist)

    mc_hist_total = sum(mc_hist_list)

    if stacked:
        plot_hist(
            mc_hist_list,
            ax=ax,
            stacked=True,
            edgecolor="black",
            histtype="stepfilled",
            linewidth=0.5,
            color=mc_colors,
            label=mc_labels,
        )
    else:
        # Plot the unstacked histograms
        plot_hist(
            mc_hist_list,
            ax=ax,
            color=mc_colors,
            label=mc_labels,
            stacked=False,
            alpha=0.8,
            histtype="stepfilled",
        )
        # Replot the unstacked histograms, but only the edges
        plot_hist(
            mc_hist_list,
            ax=ax,
            color=mc_colors,
            label=None,
            stacked=False,
            histtype="step",
        )
        # Plot the sum of the unstacked histograms
        plot_hist(
            mc_hist_total,
            ax=ax,
            color="navy",
            label="Sum(MC)",
            histtype="step",
        )
    if signal_hist is not None:
        plot_hist(
            signal_hist,
            ax=ax,
            stacked=False,
            color="red",
            label=signal_label,
            histtype="step",
        )

    xlim = (mc_hist_list[0].axes[0].edges[0], mc_hist_list[0].axes[0].edges[-1])
    ax.set_xlim(xlim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", labelbottom="off")
    ax.legend(ncol=leg_ncol)

    if save_as is not None:
        fig.savefig(save_as, bbox_inches="tight")

    return fig, ax


def add_luminosity(
    collaboration="Belle II",
    x=1.0,
    y=1.01,
    fontsize=12,
    is_data=True,
    lumi=362,
    lumi_unit="fb",
    preliminary=False,
    two_lines=False,
    white_background=False,
    ax=None,
    **kwargs,
):
    """
    Add the collaboration name and the integrated luminosity (or "Simulation").

    Parameters
    ----------
    collaboration : str, optional
        Collaboration name, by default "Belle II"
    x : float, optional
        x position, by default 1.0.
    y : float, optional
        y position, by default 1.01.
    fontsize : int, optional
        Font size, by default 12.
    is_data : bool, optional
        If True, plot integrated luminosity. If False, plot "Simulation", by default True.
    lumi : int/string, optional
        Integrated luminosity. Default value is 362. If empty, do not plot luminosity.
    lumi_unit : string, optional
        Integrated luminosity unit. Default value is fb. The exponent is automatically -1.
    preliminary : bool, optional
        If True, print "preliminary", by default False.
    two_lines : bool, optional
        If True, write the information on two lines, by default False.
    white_background : bool, optional
        Draw a white rectangle under the logo, by default False.
    ax : matplotlib.axes.Axes, optional
        Figure axis, by default None.
    kwargs : dict
        Keyword arguments to be passed to the text function.

    Returns
    -------
    None
    """
    if ax is None:
        ax = plt.gca()
    transform = ax.transAxes

    s = (
        r"$\mathrm{\mathbf{"
        + collaboration.replace(" ", "\,\,")
        + "}"
        + (r"\,\,preliminary}$" if preliminary else "}$")
    )
    if two_lines:
        s += "\n"
    else:
        s += " "
    if is_data:
        if lumi:
            s += rf"$\int\,\mathcal{{L}}\,dt={lumi}\,{lumi_unit}^{{-1}}$"
    else:
        s += r"$\mathrm{\mathbf{simulation}}$"

    t = ax.text(
        x,
        y,
        s,
        fontsize=fontsize,
        ha="right",
        va="bottom",
        transform=transform,
        **kwargs,
    )

    # Add background
    if white_background:
        t.set_bbox(dict(facecolor="white", edgecolor="white"))
