"""
Collection of functions to plot histograms in the context of High Energy Physics
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from plothist.plotters import plot_hist
from plothist.plotters import plot_error_hist
from plothist.plotters import _flatten_2d_hist


def compare_data_mc(
    data_hist,
    mc_hist_list,
    signal_hist=None,
    xlabel=None,
    ylabel=None,
    mc_labels=None,
    mc_colors=None,
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
    ax_comparison : matplotlib.axes.Axes
        Axes instance for the comparison plot.
    ax_ratio : matplotlib.axes.Axes
        Axes instance for the ratio plot.
    """
    if flatten_2d_hist:
        data_hist = _flatten_2d_hist(data_hist)
        mc_hist_list = [_flatten_2d_hist(h) for h in mc_hist_list]
        if signal_hist:
            signal_hist = _flatten_2d_hist(signal_hist)

    fig, (ax_comparison, ax_ratio) = plt.subplots(
        2, gridspec_kw={"height_ratios": [4, 1]}
    )

    xlim = (data_hist.axes[0].edges[0], data_hist.axes[0].edges[-1])
    if stacked:
        plot_hist(
            mc_hist_list,
            ax=ax_comparison,
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
            ax=ax_comparison,
            color=mc_colors,
            label=mc_labels,
            stacked=False,
            alpha=0.8,
            histtype="stepfilled",
        )
        # Replot the unstacked histograms, but only the edges
        plot_hist(
            mc_hist_list,
            ax=ax_comparison,
            color=mc_colors,
            label=None,
            stacked=False,
            histtype="step",
        )
        # Plot the sum of the unstacked histograms
        plot_hist(
            sum(mc_hist_list),
            ax=ax_comparison,
            color="navy",
            label="Sum(MC)",
            histtype="step",
        )
    if signal_hist is not None:
        plot_hist(
            signal_hist,
            ax=ax_comparison,
            stacked=False,
            color="red",
            label="Signal",
            histtype="step",
        )
    plot_error_hist(data_hist, ax=ax_comparison, color="black", label="Data")

    ax_comparison.set_xlim(xlim)
    ax_comparison.set_ylabel(ylabel)
    ax_comparison.tick_params(axis="x", labelbottom="off")

    mc_hist_total = sum(mc_hist_list)

    # Plot MC statistical uncertainty
    mc_uncertainty = np.sqrt(mc_hist_total.variances())
    ax_comparison.bar(
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

    ax_comparison.legend(framealpha=0.5)

    # Ignore divide-by-zero warning
    np.seterr(divide="ignore", invalid="ignore")
    # Compute data/MC ratio
    ratio = np.where(
        mc_hist_total.values() != 0, data_hist.values() / mc_hist_total.values(), np.nan
    )
    # Compute scaled uncertainties
    scaled_data_uncertainty = np.sqrt(data_hist.variances()) / data_hist.values()
    scaled_mc_uncertainty = np.sqrt(mc_hist_total.variances()) / mc_hist_total.values()
    # Turn on divide-by-zero warning
    np.seterr(divide="warn", invalid="warn")

    # Plot the ratio with the (scaled) statistical uncertainty of data
    ax_ratio.errorbar(
        x=mc_hist_total.axes[0].centers,
        xerr=0,
        y=np.nan_to_num(ratio, nan=0),
        yerr=np.nan_to_num(scaled_data_uncertainty, nan=0),
        fmt=".",
        color="black",
    )

    # Plot the (scaled) statistical uncertainty of simulation as a hashed area
    ax_ratio.bar(
        x=mc_hist_total.axes[0].centers,
        bottom=np.nan_to_num(1 - scaled_mc_uncertainty, nan=0),
        height=np.nan_to_num(2 * scaled_mc_uncertainty, nan=100),
        width=mc_hist_total.axes[0].widths,
        edgecolor="dimgrey",
        hatch="////",
        fill=False,
        lw=0,
    )

    ax_ratio.axhline(1, ls="--", lw=1.0, color="black")
    ax_ratio.set_ylim(0.0, 2.0)
    ax_ratio.set_xlim(xlim)
    ax_ratio.set_xlabel(xlabel)
    ax_ratio.set_ylabel(r"$\frac{Data}{Simulation}$")

    _ = ax_comparison.xaxis.set_ticklabels([])
    fig.subplots_adjust(hspace=0.12)

    if save_as is not None:
        fig.savefig(save_as, bbox_inches="tight")

    return fig, ax_comparison, ax_ratio


def plot_mc(
    mc_hist_list,
    signal_hist=None,
    xlabel=None,
    ylabel=None,
    mc_labels=None,
    mc_colors=None,
    signal_label="Signal",
    save_as=None,
    flatten_2d_hist=False,
):
    """
    Plot Monte Carlo (MC) simulations.

    Parameters
    ----------
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
    signal_label : str, optional
        Label for the signal histogram, by default "Signal".
    save_as : str, optional
        File path to save the figure, by default None.
    flatten_2d_hist : bool, optional
        Whether to flatten 2D histograms, by default False.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The generated figure.
    ax : matplotlib.axes.Axes
        Axes instance for the plot.
    """

    if flatten_2d_hist:
        mc_hist_list = [_flatten_2d_hist(h) for h in mc_hist_list]
        if signal_hist:
            signal_hist = _flatten_2d_hist(signal_hist)

    fig, ax = plt.subplots()

    xlim = (mc_hist_list[0].axes[0].edges[0], mc_hist_list[0].axes[0].edges[-1])

    plot_hist(
        mc_hist_list,
        ax=ax,
        stacked=True,
        color=mc_colors,
        label=mc_labels,
        histtype="stepfilled",
        edgecolor="black",
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

    ax.set_xlim(xlim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", labelbottom="off")
    ax.legend(framealpha=0.5, ncol=2)

    if save_as is not None:
        fig.savefig(save_as, bbox_inches="tight")

    return fig, ax


def plot_b2_logo(
    x=0.6,
    y=1.03,
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
    Plot the Belle II logo and the integrated luminosity (or "Simulation").

    Parameters
    ----------
    x : float, optional
        x position, by default 0.6.
    y : float, optional
        y position, by default 1.03.
    fontsize : int, optional
        Font size, by default 12.
    is_data : bool, optional
        If True, plot integrated luminosity. If False, plot "Simulation", by default True.
    lumi : int, optional
        Integrated luminosity. Default value is 362. If empty, do not plot luminosity.
    lumi_unit : string, optional
        Integrated luminosity unit. Default value is fb-1.
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

    s = r"$\mathrm{\mathbf{Belle\,\,II}" + (
        r"\,\,preliminary}$" if preliminary else "}$"
    )
    if two_lines:
        s += "\n"
    else:
        s += " "
    if is_data:
        if lumi:
            s += rf"$\int\,\mathcal{{L}}\,\mathrm{{d}}t={lumi}\,\mathrm{{{lumi_unit}}}^{{-1}}$"
    else:
        s += r"$\mathrm{\mathbf{simulation}}$"

    t = ax.text(x, y, s, fontsize=fontsize, transform=transform, **kwargs)
    # Add background
    if white_background:
        t.set_bbox(dict(facecolor="white", edgecolor="white"))
