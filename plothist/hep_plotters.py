""" Collection of functions to plot histograms in the context of High Energy Physics
"""

import numpy as np
import matplotlib.pyplot as plt
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
    """Compare data to mc.
    The binning among all the histograms should be equal
    Returns
    -------
    fig, ax_comparison, ax_ratio
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

    ax_comparison.legend(framealpha=0.5, fontsize=10)

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
    ax_ratio.set_ylabel(r"$\frac{Data}{Simulation}$", fontsize=18)

    _ = ax_comparison.xaxis.set_ticklabels([])

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
    """Plot mc.
    The binning among all the histograms should be equal
    Returns
    -------
    fig, ax
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
    ax.legend(framealpha=0.5, fontsize=10, ncol=2)

    if save_as is not None:
        fig.savefig(save_as, bbox_inches="tight")

    return fig, ax


def plot_b2_logo(
    x=0.6,
    y=1.03,
    fontsize=12,
    is_data=True,
    lumi="362",
    preliminary=False,
    two_lines=False,
    white_background=False,
    ax=None,
    **kwargs
):
    """
    plot the Belle II logo and the integrated luminosity (or "Simulation").

    Parameters
    ----------
    x : x position
    y : y position
    fontsize : fontsize
    is_data : if True, plot int. luminosity. If False, plot "Simulation".
    lumi : Integrated luminosity in fb-1 as a string. Default value is "63+9". If empty, do not plot luminosity.
    preliminary : If True (default), print preliminary
    two_lines : If True (default), write the information on two lines
    white_background : draw white rectangle under the logo
    ax : figure axis
    kwargs : kwargs to be passed to the text function
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
            s += r"$\int\,\mathcal{L}\,\mathrm{d}t=" + lumi + r"\,\mathrm{fb}^{-1}$"
    else:
        s += r"$\mathrm{\mathbf{simulation}}$"

    t = ax.text(x, y, s, fontsize=fontsize, transform=transform, **kwargs)
    # Add background
    if white_background:
        t.set_bbox(dict(facecolor="white", edgecolor="white"))
