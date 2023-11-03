import numpy as np
import scipy.stats as stats


def _is_unweighted(hist):
    """
    Check whether a histogram is unweighted.

    Parameters
    ----------
    hist : boost_histogram.Histogram
        The histogram to check.

    Returns
    -------
    bool
        True if the histogram is unweighted, False otherwise.
    """
    return np.allclose(hist.variances(), hist.values())


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

    Raise
    -----
    ValueError
        If the histogram is weighted.

    """
    if not _is_unweighted(data_hist):
        raise ValueError(
            "Poisson uncertainties make sense only for unweighted histograms."
        )
    conf_level = 0.682689492
    alpha = 1.0 - conf_level
    n = data_hist.values()
    uncertainties_low = n - stats.gamma.ppf(alpha / 2, n, scale=1)
    uncertainties_high = stats.gamma.ppf(1 - alpha / 2, n + 1, scale=1) - n

    return uncertainties_low, uncertainties_high


def _check_binning_consistency(hist_list):
    """
    Check that all the histograms in the provided list share the same definition of their bins.

    Parameters
    ----------
    hist_list : list of boost_histogram.Histogram
        The list of histograms to check.

    Raise
    -----
    ValueError
        If the histograms do not share the same dimensionality or if their bins are not equal.

    """
    for h in hist_list:
        if not len(h.axes) == len(hist_list[0].axes):
            raise ValueError("Histograms must have same dimensionality.")
        for i in range(len(h.axes)):
            if not h.axes[i] == hist_list[0].axes[i]:
                raise ValueError("The bins of the histograms must be equal.")


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

    _check_binning_consistency([hist_1, hist_2])

    np.seterr(divide="ignore", invalid="ignore")
    ratio_variances = np.where(
        hist_2.values() != 0,
        hist_1.variances() / hist_2.values() ** 2
        + hist_2.variances() * hist_1.values() ** 2 / hist_2.values() ** 4,
        np.nan,
    )
    np.seterr(divide="warn", invalid="warn")

    return ratio_variances


def compute_pull(hist_1, hist_2, poisson_for_hist_1=False):
    """
    Compute the pull between two histograms.

    Parameters
    ----------
    hist_1 : boost_histogram.Histogram
        The first histogram.
    hist_2 : boost_histogram.Histogram
        The second histogram.
    poisson_for_hist_1 : bool, optional
        Whether to use Poisson uncertainties for hist_1. Default is False.

    Returns
    -------
    comparison_values : numpy.ndarray
        The pull values.
    comparison_uncertainties_low : numpy.ndarray
        The lower uncertainties on the pull. Always ones.
    comparison_uncertainties_high : numpy.ndarray
        The upper uncertainties on the pull. Always ones.
    """
    if poisson_for_hist_1:
        uncertainties_low, uncertainties_high = _get_poisson_uncertainties(hist_1)
        hist_1_variances = np.where(
            hist_1.values() >= hist_2.values(),
            uncertainties_low**2,
            uncertainties_high**2,
        )
        hist_1 = hist_1.copy()
        hist_1[:] = np.c_[hist_1.values(), hist_1_variances]

    comparison_values = np.where(
        hist_1.variances() + hist_2.variances() != 0,
        (hist_1.values() - hist_2.values())
        / np.sqrt(hist_1.variances() + hist_2.variances()),
        np.nan,
    )
    comparison_uncertainties_low = np.ones_like(comparison_values)
    comparison_uncertainties_high = comparison_uncertainties_low

    return (
        comparison_values,
        comparison_uncertainties_low,
        comparison_uncertainties_high,
    )


def compute_difference(hist_1, hist_2, poisson_for_hist_1=False):
    """
    Compute the difference between two histograms.

    Parameters
    ----------
    hist_1 : boost_histogram.Histogram
        The first histogram.
    hist_2 : boost_histogram.Histogram
        The second histogram.
    poisson_for_hist_1 : bool, optional
        Whether to use Poisson uncertainties for hist_1. Default is False.

    Returns
    -------
    comparison_values : numpy.ndarray
        The difference values.
    comparison_uncertainties_low : numpy.ndarray
        The lower uncertainties on the difference.
    comparison_uncertainties_high : numpy.ndarray
        The upper uncertainties on the difference.
    """
    comparison_values = hist_1.values() - hist_2.values()

    if poisson_for_hist_1:
        uncertainties_low, uncertainties_high = _get_poisson_uncertainties(hist_1)

        comparison_uncertainties_low = np.sqrt(
            uncertainties_low**2 + hist_2.variances()
        )
        comparison_uncertainties_high = np.sqrt(
            uncertainties_high**2 + hist_2.variances()
        )
    else:
        comparison_uncertainties_low = np.sqrt(hist_1.variances() + hist_2.variances())
        comparison_uncertainties_high = comparison_uncertainties_low

    return (
        comparison_values,
        comparison_uncertainties_low,
        comparison_uncertainties_high,
    )


def compute_ratio(
    hist_1, hist_2, ratio_uncertainty="uncorrelated", poisson_for_hist_1=False
):
    """
    Compute the ratio between two histograms.

    Parameters
    ----------
    hist_1 : boost_histogram.Histogram
        The numerator histogram.
    hist_2 : boost_histogram.Histogram
        The denominator histogram.
    ratio_uncertainty : str, optional
        How to treat the uncertainties of the histograms: "uncorrelated" for simple comparison, "split" for scaling and split hist_1 and hist_2 uncertainties. Default is "uncorrelated".
    poisson_for_hist_1 : bool, optional
        Whether to use Poisson uncertainties for hist_1. Default is False.

    Returns
    -------
    comparison_values : numpy.ndarray
        The ratio values.
    comparison_uncertainties_low : numpy.ndarray
        The lower uncertainties on the ratio.
    comparison_uncertainties_high : numpy.ndarray
        The upper uncertainties on the ratio.
    """

    comparison_values = np.where(
        hist_2.values() != 0, hist_1.values() / hist_2.values(), np.nan
    )

    if poisson_for_hist_1:
        uncertainties_low, uncertainties_high = _get_poisson_uncertainties(hist_1)

    if ratio_uncertainty == "uncorrelated":
        if poisson_for_hist_1:
            hist_1_high = hist_1.copy()
            hist_1_high[:] = np.c_[hist_1_high.values(), uncertainties_high**2]
            hist_1_low = hist_1.copy()
            hist_1_low[:] = np.c_[hist_1_low.values(), uncertainties_low**2]
            comparison_uncertainties_low = np.sqrt(
                _hist_ratio_variances(hist_1_low, hist_2)
            )
            comparison_uncertainties_high = np.sqrt(
                _hist_ratio_variances(hist_1_high, hist_2)
            )
        else:
            comparison_uncertainties_low = np.sqrt(
                _hist_ratio_variances(hist_1, hist_2)
            )
            comparison_uncertainties_high = comparison_uncertainties_low
    elif ratio_uncertainty == "split":
        if poisson_for_hist_1:
            comparison_uncertainties_low = uncertainties_low / hist_2.values()
            comparison_uncertainties_high = uncertainties_high / hist_2.values()
        else:
            h1_scaled_uncertainties = np.where(
                hist_2.values() != 0,
                np.sqrt(hist_1.variances()) / hist_2.values(),
                np.nan,
            )
            comparison_uncertainties_low = h1_scaled_uncertainties
            comparison_uncertainties_high = comparison_uncertainties_low
    else:
        raise ValueError("ratio_uncertainty not in ['uncorrelated', 'split'].")

    return (
        comparison_values,
        comparison_uncertainties_low,
        comparison_uncertainties_high,
    )


def compute_comparison(
    hist_1,
    hist_2,
    comparison,
    ratio_uncertainty="uncorrelated",
    poisson_for_hist_1=False,
):
    """
    Compute the comparison between two histograms.

    Parameters
    ----------
    hist_1 : boost_histogram.Histogram
        The first histogram for comparison.
    hist_2 : boost_histogram.Histogram
        The second histogram for comparison.
    comparison : str
        The type of comparison to plot ("ratio", "pull", "difference" or "relative_difference").
    ratio_uncertainty : str, optional
        How to treat the uncertainties of the histograms when comparison is "ratio" or "relative_difference" ("uncorrelated" for simple comparison, "split" for scaling and split hist_1 and hist_2 uncertainties). This argument has no effect if comparison != "ratio" or "relative_difference". Default is "uncorrelated".
    poisson_for_hist_1 : bool, optional
        Whether to use Poisson uncertainties for hist_1. Default is False.

    Returns
    -------
    values : numpy.ndarray
        The comparison values.
    lower_uncertainties : numpy.ndarray
        The lower uncertainties on the comparison values.
    upper_uncertainties : numpy.ndarray
        The upper uncertainties on the comparison values.
    """

    _check_binning_consistency([hist_1, hist_2])

    np.seterr(divide="ignore", invalid="ignore")

    if comparison == "ratio":
        values, lower_uncertainties, upper_uncertainties = compute_ratio(
            hist_1, hist_2, ratio_uncertainty, poisson_for_hist_1
        )
    elif comparison == "relative_difference":
        values, lower_uncertainties, upper_uncertainties = compute_ratio(
            hist_1, hist_2, ratio_uncertainty, poisson_for_hist_1
        )
        values -= 1  # relative difference is ratio-1
    elif comparison == "pull":
        values, lower_uncertainties, upper_uncertainties = compute_pull(
            hist_1, hist_2, poisson_for_hist_1
        )
    elif comparison == "difference":
        values, lower_uncertainties, upper_uncertainties = compute_difference(
            hist_1, hist_2, poisson_for_hist_1
        )
    else:
        raise ValueError(
            f"{comparison} not available as a comparison ('ratio', 'pull', 'difference' or 'relative_difference')."
        )
    np.seterr(divide="warn", invalid="warn")

    return values, lower_uncertainties, upper_uncertainties
