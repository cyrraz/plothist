import numpy as np
import scipy.stats as stats

from plothist.histogramming import _check_counting_histogram


def _check_uncertainty_type(uncertainty_type):
    """
    Check that the uncertainty type is valid.

    Parameters
    ----------
    uncertainty_type : str
        The uncertainty type to check.

    Raise
    -----
    ValueError
        If the uncertainty type is not valid.

    """
    if uncertainty_type not in ["symmetrical", "asymmetrical"]:
        raise ValueError(
            f"Uncertainty type {uncertainty_type} not valid. Must be 'symmetrical' or 'asymmetrical'."
        )


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


def get_asymmetrical_uncertainties(hist):
    """
    Get Poisson asymmetrical uncertainties for a histogram via a frequentist approach based on a confidence-interval computation.
    Asymmetrical uncertainties can only be computed for an unweighted histogram, because the bin contents of a weighted histogram do not follow a Poisson distribution.
    More information in :ref:`documentation-statistics-label`.

    Parameters
    ----------
    hist : boost_histogram.Histogram
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
    _check_counting_histogram(hist)

    if not _is_unweighted(hist):
        raise ValueError(
            "Asymmetrical uncertainties can only be computed for an unweighted histogram."
        )
    conf_level = 0.682689492
    alpha = 1.0 - conf_level
    n = hist.values()
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


def get_ratio_variances(h1, h2):
    """
    Calculate the variances of the ratio of two uncorrelated histograms (h1/h2).

    Parameters
    ----------
    h1 : boost_histogram.Histogram
        The first histogram.
    h2 : boost_histogram.Histogram
        The second histogram.

    Returns
    -------
    ratio_variances : np.ndarray
        The variances of the ratio of the two histograms.

    Raises
    ------
    ValueError
        If the bins of the histograms are not equal.
    """
    _check_binning_consistency([h1, h2])
    _check_counting_histogram(h1)
    _check_counting_histogram(h2)

    np.seterr(divide="ignore", invalid="ignore")
    ratio_variances = np.where(
        h2.values() != 0,
        h1.variances() / h2.values() ** 2
        + h2.variances() * h1.values() ** 2 / h2.values() ** 4,
        np.nan,
    )
    np.seterr(divide="warn", invalid="warn")

    return ratio_variances


def get_pull(h1, h2, h1_uncertainty_type="symmetrical"):
    """
    Compute the pull between two histograms.

    Parameters
    ----------
    h1 : boost_histogram.Histogram
        The first histogram.
    h2 : boost_histogram.Histogram
        The second histogram.
    h1_uncertainty_type : str, optional
        What kind of bin uncertainty to use for h1: "symmetrical" for the Poisson standard deviation derived from the variance stored in the histogram object, "asymmetrical" for asymmetrical uncertainties based on a Poisson confidence interval. Default is "symmetrical".

    Returns
    -------
    pull_values : numpy.ndarray
        The pull values.
    pull_uncertainties_low : numpy.ndarray
        The lower uncertainties on the pull. Always ones.
    pull_uncertainties_high : numpy.ndarray
        The upper uncertainties on the pull. Always ones.
    """
    _check_uncertainty_type(h1_uncertainty_type)
    _check_binning_consistency([h1, h2])
    _check_counting_histogram(h1)
    _check_counting_histogram(h2)

    if h1_uncertainty_type == "asymmetrical":
        uncertainties_low, uncertainties_high = get_asymmetrical_uncertainties(h1)
        h1_variances = np.where(
            h1.values() >= h2.values(),
            uncertainties_low**2,
            uncertainties_high**2,
        )
        h1 = h1.copy()
        h1[:] = np.c_[h1.values(), h1_variances]

    pull_values = np.where(
        h1.variances() + h2.variances() != 0,
        (h1.values() - h2.values()) / np.sqrt(h1.variances() + h2.variances()),
        np.nan,
    )
    pull_uncertainties_low = np.ones_like(pull_values)
    pull_uncertainties_high = pull_uncertainties_low

    return (
        pull_values,
        pull_uncertainties_low,
        pull_uncertainties_high,
    )


def get_difference(h1, h2, h1_uncertainty_type="symmetrical"):
    """
    Compute the difference between two histograms.

    Parameters
    ----------
    h1 : boost_histogram.Histogram
        The first histogram.
    h2 : boost_histogram.Histogram
        The second histogram.
    h1_uncertainty_type : str, optional
        What kind of bin uncertainty to use for h1: "symmetrical" for the Poisson standard deviation derived from the variance stored in the histogram object, "asymmetrical" for asymmetrical uncertainties based on a Poisson confidence interval. Default is "symmetrical".

    Returns
    -------
    difference_values : numpy.ndarray
        The difference values.
    difference_uncertainties_low : numpy.ndarray
        The lower uncertainties on the difference.
    difference_uncertainties_high : numpy.ndarray
        The upper uncertainties on the difference.
    """
    _check_uncertainty_type(h1_uncertainty_type)
    _check_binning_consistency([h1, h2])
    _check_counting_histogram(h1)
    _check_counting_histogram(h2)

    difference_values = h1.values() - h2.values()

    if h1_uncertainty_type == "asymmetrical":
        uncertainties_low, uncertainties_high = get_asymmetrical_uncertainties(h1)

        difference_uncertainties_low = np.sqrt(uncertainties_low**2 + h2.variances())
        difference_uncertainties_high = np.sqrt(uncertainties_high**2 + h2.variances())
    else:
        difference_uncertainties_low = np.sqrt(h1.variances() + h2.variances())
        difference_uncertainties_high = difference_uncertainties_low

    return (
        difference_values,
        difference_uncertainties_low,
        difference_uncertainties_high,
    )


def get_efficency(h1, h2):
    """
    Calculate the ratio of two correlated histograms (h1/h2), in which the entries of h1 are a subsample of the entries of h2.
    The variances are calculated according to the formula given in :ref:`documentation-statistics-label`.

    The following conditions must be fulfilled for the calculation of the efficiency:
    * The bins of the histograms must be equal.
    * The histograms must be unweighted.
    * The bin contents of both histograms must be positive or zero.
    * The bin contents of h1 must be a subsample of the bin contents of h2.

    Parameters
    ----------
    h1 : boost_histogram.Histogram
        The first histogram.
    h2 : boost_histogram.Histogram
        The second histogram.

    Returns
    -------
    efficiency_values : numpy.ndarray
        The efficiency values.
    efficiency_uncertainties : numpy.ndarray
        The uncertainties on the efficiency values.

    Raises
    ------
    ValueError
        If the histograms are weighted.
    ValueError
        If the bin contents of the histograms are not positive or zero.
    ValueError
        If the bin contents of h1 are not a subsample of the bin contents of h2.
    """
    _check_binning_consistency([h1, h2])
    _check_counting_histogram(h1)
    _check_counting_histogram(h2)

    if not (_is_unweighted(h1) and _is_unweighted(h2)):
        raise ValueError(
            "The ratio of two correlated histograms (efficiency) can only be computed for unweighted histograms."
        )
    if not (np.all(h1.values() >= 0) and np.all(h2.values() >= 0)):
        raise ValueError(
            "The ratio of two correlated histograms (efficiency) can only be computed if the bin contents of both histograms are positive or zero."
        )
    if not np.all(h1.values() <= h2.values()):
        raise ValueError(
            "The ratio of two correlated histograms (efficiency) can only be computed if the bin contents of h1 are a subsample of the bin contents of h2."
        )

    efficiency_values = np.where(h2.values() != 0, h1.values() / h2.values(), np.nan)

    k = h1.values()
    n = h2.values()

    efficiency_variances = (k + 1) * (k + 2) / (n + 2) / (n + 3) - (k + 1) ** 2 / (
        n + 2
    ) ** 2

    return efficiency_values, np.sqrt(efficiency_variances)


def get_asymmetry(h1, h2):
    """
    Get the asymmetry between two histograms h1 and h2, defined as (h1 - h2) / (h1 + h2).
    Only symmetrical uncertainties are supported.

    Parameters
    ----------
    h1 : boost_histogram.Histogram
        The first histogram.
    h2 : boost_histogram.Histogram
        The second histogram.

    Returns
    -------
    asymmetry_values : numpy.ndarray
        The asymmetry values.
    asymmetry_uncertainties : numpy.ndarray
        The uncertainties on the asymmetry.
    """
    _check_binning_consistency([h1, h2])
    _check_counting_histogram(h1)
    _check_counting_histogram(h2)

    hist_sum = h1 + h2
    hist_diff = h1 + (-1 * h2)
    asymmetry_values = np.where(
        hist_sum.values() != 0, hist_diff.values() / hist_sum.values(), np.nan
    )
    asymmetry_variances = get_ratio_variances(hist_diff, hist_sum)
    return (
        asymmetry_values,
        np.sqrt(asymmetry_variances),
    )


def get_ratio(
    h1,
    h2,
    h1_uncertainty_type="symmetrical",
    ratio_uncertainty_type="uncorrelated",
):
    """
    Compute the ratio h1/h2 between two uncorrelated histograms h1 and h2.

    Parameters
    ----------
    h1 : boost_histogram.Histogram
        The numerator histogram.
    h2 : boost_histogram.Histogram
        The denominator histogram.
    h1_uncertainty_type : str, optional
        What kind of bin uncertainty to use for h1: "symmetrical" for the Poisson standard deviation derived from the variance stored in the histogram object, "asymmetrical" for asymmetrical uncertainties based on a Poisson confidence interval. Default is "symmetrical".
    ratio_uncertainty_type : str, optional
        How to treat the uncertainties of the histograms:
        * "uncorrelated" for the comparison of two uncorrelated histograms,
        * "split" for scaling down the uncertainties of h1 by bin contents of h2, i.e. assuming zero uncertainty coming from h2 in the ratio uncertainty.
        Default is "uncorrelated".

    Returns
    -------
    ratio_values : numpy.ndarray
        The ratio values.
    ratio_uncertainties_low : numpy.ndarray
        The lower uncertainties on the ratio.
    ratio_uncertainties_high : numpy.ndarray
        The upper uncertainties on the ratio.

    Raises
    ------
    ValueError
        If the ratio_uncertainty_type is not valid.
    """
    _check_uncertainty_type(h1_uncertainty_type)
    _check_binning_consistency([h1, h2])
    _check_counting_histogram(h1)
    _check_counting_histogram(h2)

    ratio_values = np.where(h2.values() != 0, h1.values() / h2.values(), np.nan)

    if h1_uncertainty_type == "asymmetrical":
        uncertainties_low, uncertainties_high = get_asymmetrical_uncertainties(h1)

    if ratio_uncertainty_type == "uncorrelated":
        if h1_uncertainty_type == "asymmetrical":
            h1_high = h1.copy()
            h1_high[:] = np.c_[h1_high.values(), uncertainties_high**2]
            h1_low = h1.copy()
            h1_low[:] = np.c_[h1_low.values(), uncertainties_low**2]
            ratio_uncertainties_low = np.sqrt(get_ratio_variances(h1_low, h2))
            ratio_uncertainties_high = np.sqrt(get_ratio_variances(h1_high, h2))
        else:
            ratio_uncertainties_low = np.sqrt(get_ratio_variances(h1, h2))
            ratio_uncertainties_high = ratio_uncertainties_low
    elif ratio_uncertainty_type == "split":
        if h1_uncertainty_type == "asymmetrical":
            ratio_uncertainties_low = uncertainties_low / h2.values()
            ratio_uncertainties_high = uncertainties_high / h2.values()
        else:
            h1_scaled_uncertainties = np.where(
                h2.values() != 0,
                np.sqrt(h1.variances()) / h2.values(),
                np.nan,
            )
            ratio_uncertainties_low = h1_scaled_uncertainties
            ratio_uncertainties_high = ratio_uncertainties_low
    else:
        raise ValueError("ratio_uncertainty_type not in ['uncorrelated', 'split'].")

    return (
        ratio_values,
        ratio_uncertainties_low,
        ratio_uncertainties_high,
    )


def get_comparison(
    h1,
    h2,
    comparison,
    h1_uncertainty_type="symmetrical",
):
    """
    Compute the comparison between two histograms.

    Parameters
    ----------
    h1 : boost_histogram.Histogram
        The first histogram for comparison.
    h2 : boost_histogram.Histogram
        The second histogram for comparison.
    comparison : str
        The type of comparison ("ratio", "split_ratio", "pull", "difference", "relative_difference", "efficiency", or "asymmetry").
        When the `split_ratio` option is used, the uncertainties of h1 are scaled down by the bin contents of h2, i.e. assuming zero uncertainty coming from h2 in the ratio uncertainty.
    h1_uncertainty_type : str, optional
        What kind of bin uncertainty to use for h1: "symmetrical" for the Poisson standard deviation derived from the variance stored in the histogram object, "asymmetrical" for asymmetrical uncertainties based on a Poisson confidence interval.
        Asymmetrical uncertainties are not supported for the asymmetry and efficiency comparisons.
        Default is "symmetrical".

    Returns
    -------
    values : numpy.ndarray
        The comparison values.
    lower_uncertainties : numpy.ndarray
        The lower uncertainties on the comparison values.
    upper_uncertainties : numpy.ndarray
        The upper uncertainties on the comparison values.

    Raises
    ------
    ValueError
        If the comparison is not valid.
    ValueError
        If the h1_uncertainty_type is "asymmetrical" and the comparison is "asymmetry" or "efficiency".
    """
    _check_uncertainty_type(h1_uncertainty_type)
    _check_binning_consistency([h1, h2])
    _check_counting_histogram(h1)
    _check_counting_histogram(h2)

    np.seterr(divide="ignore", invalid="ignore")

    if comparison == "ratio":
        values, lower_uncertainties, upper_uncertainties = get_ratio(
            h1, h2, h1_uncertainty_type, "uncorrelated"
        )
    elif comparison == "split_ratio":
        values, lower_uncertainties, upper_uncertainties = get_ratio(
            h1, h2, h1_uncertainty_type, "split"
        )
    elif comparison == "relative_difference":
        values, lower_uncertainties, upper_uncertainties = get_ratio(
            h1, h2, h1_uncertainty_type, "uncorrelated"
        )
        values -= 1  # relative difference is ratio-1
    elif comparison == "pull":
        values, lower_uncertainties, upper_uncertainties = get_pull(
            h1, h2, h1_uncertainty_type
        )
    elif comparison == "difference":
        values, lower_uncertainties, upper_uncertainties = get_difference(
            h1, h2, h1_uncertainty_type
        )
    elif comparison == "asymmetry":
        if h1_uncertainty_type == "asymmetrical":
            raise ValueError(
                "Asymmetrical uncertainties are not supported for the asymmetry comparison."
            )
        values, uncertainties = get_asymmetry(h1, h2)
        lower_uncertainties = uncertainties
        upper_uncertainties = uncertainties
    elif comparison == "efficiency":
        if h1_uncertainty_type == "asymmetrical":
            raise ValueError(
                "Asymmetrical uncertainties are not supported in an efficiency computation."
            )
        values, uncertainties = get_efficency(h1, h2)
        lower_uncertainties = uncertainties
        upper_uncertainties = uncertainties
    else:
        raise ValueError(
            f"{comparison} not available as a comparison ('ratio', 'split_ratio', 'pull', 'difference', 'relative_difference', 'asymmetry' or 'efficiency')."
        )
    np.seterr(divide="warn", invalid="warn")

    return values, lower_uncertainties, upper_uncertainties
