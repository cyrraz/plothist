"""
Collection of functions to plot histograms in the context of High Energy Physics
"""
import numpy as np
import matplotlib.pyplot as plt
from plothist.plotters import (
    plot_hist,
    plot_error_hist,
    _flatten_2d_hist,
    plot_comparison,
    create_comparison_figure,
)
from plothist.plothist_style import set_fitting_ylabel_fontsize, add_text
from plothist.comparison import (
    _check_binning_consistency,
    get_asymmetrical_uncertainties,
    _is_unweighted,
)


def compare_data_mc(
    data_hist,
    mc_hist_list,
    signal_hist=None,
    xlabel=None,
    ylabel=None,
    mc_labels=None,
    mc_colors=None,
    signal_label="Signal",
    signal_color="red",
    data_label="Data",
    save_as=None,
    flatten_2d_hist=False,
    stacked=True,
    mc_uncertainty=True,
    mc_uncertainty_label="MC stat. unc.",
    fig=None,
    ax_main=None,
    ax_comparison=None,
    **comparison_kwargs,
):
    """
    Compare data to MC simulations. The data uncertainties are computed using the Poisson confidence interval.

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
    signal_label : str, optional
        The label for the signal. Default is "Signal".
    signal_color : str, optional
        The color for the signal. Default is "red".
    data_label : str, optional
        The label for the data. Default is "Data".
    save_as : str or None, optional
        The file path to save the figure. Default is None.
    flatten_2d_hist : bool, optional
        If True, flatten 2D histograms to 1D before plotting. Default is False.
    stacked : bool, optional
        If True, stack the MC histograms. If False, plot them side by side. Default is True.
    mc_uncertainty : bool, optional
        If False, set the MC uncertainties to zeros. Useful for post-fit histograms. Default is True.
    mc_uncertainty_label : str, optional
        The label for the MC uncertainties. Default is "MC stat. unc.".
    fig : matplotlib.figure.Figure or None, optional
        The figure to use for the plot. If fig, ax_main and ax_comparison are None, a new figure will be created. Default is None.
    ax_main : matplotlib.axes.Axes or None, optional
        The main axes for the histogram comparison. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    ax_comparison : matplotlib.axes.Axes or None, optional
        The axes for the comparison plot. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    **comparison_kwargs : optional
        Arguments to be passed to plot_comparison(), including the choice of the comparison function and the treatment of the uncertainties (see documentation of plot_comparison() for details). If they are not provided explicitly, the following arguments are passed by default: h1_label="Data", h2_label="Pred.", comparison="ratio", and ratio_uncertainty="split".

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
    comparison_kwargs.setdefault("h1_label", data_label)
    comparison_kwargs.setdefault("h2_label", "Pred.")
    comparison_kwargs.setdefault("comparison", "ratio")
    comparison_kwargs.setdefault("ratio_uncertainty", "split")

    _check_binning_consistency(
        mc_hist_list + [data_hist] + ([signal_hist] if signal_hist is not None else [])
    )

    if fig is None and ax_main is None and ax_comparison is None:
        fig, (ax_main, ax_comparison) = create_comparison_figure()
    elif fig is None or ax_main is None or ax_comparison is None:
        raise ValueError(
            "Need to provid fig, ax_main and ax_comparison (or none of them)."
        )

    if flatten_2d_hist:
        mc_hist_list = [_flatten_2d_hist(h) for h in mc_hist_list]
        data_hist = _flatten_2d_hist(data_hist)
        if signal_hist:
            signal_hist = _flatten_2d_hist(signal_hist)

    mc_hist_total = sum(mc_hist_list)

    plot_mc(
        mc_hist_list,
        signal_hist=signal_hist,
        ylabel=ylabel,
        mc_labels=mc_labels,
        mc_colors=mc_colors,
        signal_label=signal_label,
        signal_color=signal_color,
        fig=fig,
        ax=ax_main,
        stacked=stacked,
        flatten_2d_hist=False,  # Already done
    )

    if not mc_uncertainty:
        mc_hist_total[:] = np.c_[
            mc_hist_total.values(), np.zeros_like(mc_hist_total.values())
        ]

    # Compute data uncertainties
    if _is_unweighted(data_hist):
        # For unweighted data, use a Poisson confidence interval as uncertainty
        uncertainties_low, uncertainties_high = get_asymmetrical_uncertainties(
            data_hist
        )
        data_uncertainty = "asymmetrical"
    else:
        # Otherwise, use the Poisson standard deviation a uncertainty
        uncertainties_low = np.sqrt(data_hist.variances())
        uncertainties_high = uncertainties_low
        data_uncertainty = "symmetrical"

    plot_error_hist(
        data_hist,
        ax=ax_main,
        yerr=[uncertainties_low, uncertainties_high],
        color="black",
        label=data_label,
    )

    _ = ax_main.xaxis.set_ticklabels([])

    # Plot MC statistical uncertainty
    if mc_uncertainty:
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
            label=mc_uncertainty_label,
        )
    elif comparison_kwargs["comparison"] == "pull":
        comparison_kwargs.setdefault(
            "comparison_ylabel",
            rf"$\frac{{ {comparison_kwargs['h1_label']} - {comparison_kwargs['h2_label']} }}{{ \sigma_{{{comparison_kwargs['h1_label']}}} }} $",
        )

    ax_main.legend()

    plot_comparison(
        data_hist,
        mc_hist_total,
        ax=ax_comparison,
        xlabel=xlabel,
        hist_1_uncertainty=data_uncertainty,
        **comparison_kwargs,
    )

    ylabel_fontsize = set_fitting_ylabel_fontsize(ax_main)
    ax_comparison.get_yaxis().get_label().set_size(ylabel_fontsize)

    fig.align_ylabels()

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
    signal_color="red",
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
    signal_color : str, optional
        The color for the signal. Default is "red".
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

    _check_binning_consistency(
        mc_hist_list + ([signal_hist] if signal_hist is not None else [])
    )

    if fig is None and ax is None:
        fig, ax = plt.subplots()
    elif fig is None or ax is None:
        raise ValueError("Need to provid both fig and ax (or none).")

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
            color=signal_color,
            label=signal_label,
            histtype="step",
        )

    xlim = (mc_hist_list[0].axes[0].edges[0], mc_hist_list[0].axes[0].edges[-1])
    ax.set_xlim(xlim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    set_fitting_ylabel_fontsize(ax)
    ax.legend(ncol=leg_ncol)

    if save_as is not None:
        fig.savefig(save_as, bbox_inches="tight")

    return fig, ax


def add_luminosity(
    collaboration="Belle II",
    x="right",
    y="top",
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
        Horizontal position of the text in unit of the normalized x-axis length. The default is value "right", which is an alias for 1.0.
    y : float, optional
        Vertical position of the text in unit of the normalized y-axis length. The default is value "top", which is an alias for 1.01.
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
        Draw a white rectangle under the text, by default False.
    ax : matplotlib.axes.Axes, optional
        Figure axis, by default None.
    kwargs : dict
        Keyword arguments to be passed to the ax.text() function.
        In particular, the keyword arguments ha and va, which are set to "left" (or "right" if x="right") and "bottom" by default, can be used to change the text alignment.

    Returns
    -------
    None

    See Also
    --------
    add_text : Add information on the plot.
    """

    text = (
        r"$\mathrm{\mathbf{"
        + collaboration.replace(" ", "\,\,")
        + "}"
        + (r"\,\,preliminary}$" if preliminary else "}$")
    )
    if two_lines:
        text += "\n"
    else:
        text += " "
    if is_data:
        if lumi:
            text += rf"$\int\,\mathcal{{L}}\,\mathrm{{dt}}={lumi}\,{lumi_unit}^{{-1}}$"
    else:
        text += r"$\mathrm{\mathbf{Simulation}}$"

    add_text(
        text,
        x,
        y,
        fontsize=fontsize,
        white_background=white_background,
        ax=ax,
        **kwargs,
    )
