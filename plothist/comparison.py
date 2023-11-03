import numpy as np
import boost_histogram as bh


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


def compute_comparison(hist_1, hist_2, comparison, ratio_uncertainty="uncorrelated"):
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

    Returns
    -------
    hist_comparison : boost_histogram.Histogram
        The histogram with the comparison values and variances.
    """

    _check_binning_consistency([hist_1, hist_2])

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
        if ratio_uncertainty == "uncorrelated":
            comparison_variances = _hist_ratio_variances(hist_1, hist_2)
        elif ratio_uncertainty == "split":
            h1_scaled_uncertainties = np.where(
                hist_2.values() != 0,
                np.sqrt(hist_1.variances()) / hist_2.values(),
                np.nan,
            )
            comparison_variances = h1_scaled_uncertainties**2
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
    hist_comparison[:] = np.c_[comparison_values, comparison_variances]

    return hist_comparison
