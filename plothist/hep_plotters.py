"""
Collection of functions to plot histograms in the context of High Energy Physics
"""
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib as mpl
from plothist.plotters import (
    plot_hist,
    plot_error_hist,
    _flatten_2d_hist,
    plot_comparison,
    create_comparison_figure,
    _hist_ratio_variances,
)
from plothist.plothist_style import get_fitting_ylabel_fontsize, add_text


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

    # Compute data uncertainties
    if np.allclose(data_hist.variances(), data_hist.values()):
        # If the variances are equal to the bin contents (i.e. un-weighted data), use the Poisson confidence intervals as uncertainties
        uncertainties_low, uncertainties_high = _get_poisson_uncertainties(data_hist)
    else:
        # Otherwise, use the Gaussian uncertainties
        uncertainties_low = np.sqrt(data_hist.variances())
        uncertainties_high = uncertainties_low

    print(comparison_kwargs["comparison"], data_hist.variances())
    if comparison_kwargs["comparison"] == "pull":
        data_variances = np.where(
            data_hist.values() >= mc_hist_total.values(),
            uncertainties_low**2,
            uncertainties_high**2,
        )
        data_hist = data_hist.copy()
        data_hist[:] = np.stack([data_hist.values(), data_variances], axis=-1)
    elif comparison_kwargs["comparison"] in ["ratio", "relative_difference"]:
        if comparison_kwargs["ratio_uncertainty"] == "split":
            np.seterr(divide="ignore", invalid="ignore")
            # Compute asymmetrical uncertainties to plot_comparison()
            comparison_kwargs.setdefault(
                "yerr",
                [
                    uncertainties_low / mc_hist_total.values(),
                    uncertainties_high / mc_hist_total.values(),
                ],
            )
            np.seterr(divide="warn", invalid="warn")
        elif comparison_kwargs["ratio_uncertainty"] == "uncorrelated":
            data_hist_high = data_hist.copy()
            data_hist_high[:] = np.stack(
                [data_hist_high.values(), uncertainties_high**2], axis=-1
            )
            data_hist_low = data_hist.copy()
            data_hist_low[:] = np.stack(
                [data_hist_low.values(), uncertainties_low**2], axis=-1
            )
            # Compute asymmetrical uncertainties to plot_comparison()
            comparison_kwargs.setdefault(
                "yerr",
                [
                    np.sqrt(_hist_ratio_variances(data_hist_low, mc_hist_total)),
                    np.sqrt(_hist_ratio_variances(data_hist_high, mc_hist_total)),
                ],
            )
    elif comparison_kwargs["comparison"] == "difference":
        data_hist_high = data_hist.copy()
        data_hist_high[:] = np.stack(
            [data_hist_high.values(), uncertainties_high**2], axis=-1
        )
        data_hist_low = data_hist.copy()
        data_hist_low[:] = np.stack(
            [data_hist_low.values(), uncertainties_low**2], axis=-1
        )
        comparison_kwargs.setdefault(
            "yerr",
            [
                np.sqrt(data_hist_low.variances() + mc_hist_total.variances()),
                np.sqrt(data_hist_high.variances() + mc_hist_total.variances()),
            ],
        )
    else:
        raise ValueError(
            f"Unknown comparison {comparison_kwargs['comparison']}. Please choose from 'pull', 'ratio', 'relative_difference', or 'difference'."
        )

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
    else:
        mc_hist_total[:] = np.stack(
            [mc_hist_total.values(), np.zeros_like(mc_hist_total.values())], axis=-1
        )
        if comparison_kwargs["comparison"] == "pull":
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
        **comparison_kwargs,
    )

    ylabel_fontsize = get_fitting_ylabel_fontsize(ax_main)
    ax_main.get_yaxis().get_label().set_size(ylabel_fontsize)
    ax_comparison.get_yaxis().get_label().set_size(ylabel_fontsize)

    fig.align_ylabels()

    if save_as is not None:
        fig.savefig(save_as, bbox_inches="tight")

    return fig, ax_main, ax_comparison


def _get_poisson_uncertainties(data_hist):
    """
    Get Poisson asymmetrical uncertainties for a histogram.

    Parameters
    ----------
    data_hist : boost_histogram.Histogram
        The histogram.

    Returns
    -------
    uncertainties_low : numpy.ndarray
        The lower uncertainties.
    uncertainties_high : numpy.ndarray
        The upper uncertainties.
    """
    conf_level = 0.682689492
    alpha = 1.0 - conf_level
    n = data_hist.values()
    uncertainties_low = n - stats.gamma.ppf(alpha / 2, n, scale=1)
    uncertainties_high = stats.gamma.ppf(1 - alpha / 2, n + 1, scale=1) - n

    return uncertainties_low, uncertainties_high


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
            color=signal_color,
            label=signal_label,
            histtype="step",
        )

    xlim = (mc_hist_list[0].axes[0].edges[0], mc_hist_list[0].axes[0].edges[-1])
    ax.set_xlim(xlim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel, fontsize=get_fitting_ylabel_fontsize(ax))
    ax.tick_params(axis="x", labelbottom="off")
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
