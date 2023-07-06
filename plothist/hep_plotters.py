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
):
    """
    Compare data to MC simulations.

    Parameters
    ----------
    data_hist : boost_histogram.Histogram
        Histogram of the data.
    mc_hist_list : list of boost_histogram.Histogram
        List of histograms representing the MC simulations.
    signal_hist : boost_histogram.Histogram, optional
        Histogram representing the signal MC simulation, by default None.
    xlabel : str, optional
        Label for the x-axis, by default None.
    ylabel : str, optional
        Label for the y-axis, by default None.
    mc_labels : list of str, optional
        List of labels for the MC simulations, by default None.
    mc_colors : list of str, optional
        List of colors for the MC simulations, by default None.
    comparison: str, optional
        How to compare the two histograms.
        Available ratios: 'ratio' to compute the difference and 'pull' to compute the pulls between the two histograms
    comparison_ylim: list of float, optional
        Set the ylim of the ax_comparison. If not specified, ylim = [0., 2.] for ratio comparison and [-5., 5.] for pull.
    save_as : str, optional
        File path to save the figure, by default None.
    flatten_2d_hist : bool, optional
        Whether to flatten 2D histograms, by default False.
    stacked : bool, optional
        Whether to stack the MC histograms, by default True.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The generated figure.
    ax_main : matplotlib.axes.Axes
        Axes instance for the comparison plot.
    ax_comparison : matplotlib.axes.Axes
        Axes instance for the comparison plot.
    """

    fig, (ax_main, ax_comparison) = plt.subplots(
        2, gridspec_kw={"height_ratios": [4, 1]}
    )
    fig.subplots_adjust(hspace=0.125)

    plot_mc(
        mc_hist_list,
        signal_hist=signal_hist,
        ylabel=ylabel,
        mc_labels=mc_labels,
        mc_colors=mc_colors,
        fig=fig,
        ax=ax_main,
        flatten_2d_hist=flatten_2d_hist,
        stacked=stacked,
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

    ax_main.legend(framealpha=0.5)

    plot_comparison(
        data_hist,
        mc_hist_total,
        ax=ax_comparison,
        xlabel=xlabel,
        x1_label="Data",
        x2_label="Pred.",
        comparison=comparison,
        comparison_ylim=comparison_ylim,
        scaled_uncertainty=True,
        hist_2_uncertainty=True,
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
    leg_ncol=1
):
    """

    """

    if fig is None and ax is None:
        fig, ax = plt.subplots()
    elif fig is None:
        fig, _ = plt.subplots()
    elif ax is None:
        _, ax = plt.subplots()

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
            sum(mc_hist_list),
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
    ax.legend(framealpha=0.5, ncol=leg_ncol)

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
    lumi : int, optional
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
