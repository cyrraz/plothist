import warnings

import numpy as np
from uhi.numpy_plottable import Kind, NumPyPlottableHistogram


class EnhancedNumPyPlottableHistogram(NumPyPlottableHistogram):
    """
    A class that extends the NumPyPlottableHistogram class to allow for arithmetic operations between histograms.

    Parameters
    ----------
    hist : array-like
        The histogram values.
    bins : array-like
        The bin edges of the histogram.
    variances : array-like, optional
        The variances of the histogram values. Default is None.
    kind : Kind, optional
        The kind of histogram. Default is Kind.COUNT.
    """

    def __init__(self, hist, *bins, variances=None, kind=Kind.COUNT):
        super().__init__(hist, *bins, variances=variances, kind=kind)

    def __add__(self, other):
        if not isinstance(other, EnhancedNumPyPlottableHistogram):
            raise TypeError(
                "Can only add EnhancedNumPyPlottableHistogram to EnhancedNumPyPlottableHistogram"
            )
        if len(self.axes) > 1:
            raise NotImplementedError(
                "Addition of multi-dimensional histograms is not supported"
            )
        if self.axes != other.axes:
            raise ValueError("Histograms must have the same axes to be added")
        added_values = self.values() + other.values()
        added_variances = None
        if self._variances is not None and other._variances is not None:
            added_variances = self._variances + other._variances
        return EnhancedNumPyPlottableHistogram(
            added_values, self.axes[0].edges, variances=added_variances, kind=self.kind
        )

    def __radd__(self, other):
        if other == 0:
            return self
        return self.__add__(other)

    def __mul__(self, factor):
        if not isinstance(factor, (int, float)):
            raise TypeError("Factor must be a scalar (int or float)")
        if len(self.axes) > 1:
            raise NotImplementedError(
                "Scaling of multi-dimensional histograms is not supported"
            )
        scaled_values = self.values() * factor
        scaled_variances = None
        if self._variances is not None:
            scaled_variances = self._variances * factor**2
        return EnhancedNumPyPlottableHistogram(
            scaled_values,
            self.axes[0].edges,
            variances=scaled_variances,
            kind=self.kind,
        )

    def __rmul__(self, factor):
        return self.__mul__(factor)


# Define a custom warning for range issues
class RangeWarning(Warning):
    pass


# Always show the range warnings
warnings.filterwarnings("always", category=RangeWarning)


def make_hist(data=None, bins=50, range=None, weights=1):
    """
    Create a histogram object and fill it with the provided data.

    Parameters
    ----------
    data : array-like, optional
        1D array-like data used to fill the histogram (default is None).
        If None is provided, an empty histogram is returned.
    bins : int or tuple, optional
        Binning specification for the histogram (default is 50).
        If an integer, it represents the number of bins.
        If a tuple, it should be the explicit list of all bin edges.
    range : tuple, optional
        The range of values to consider for the histogram bins (default is None).
        If None, the range is determined from the data.
    weights : float or array-like, optional
        Weight(s) to apply to the data points (default is 1).
        If a float, a single weight is applied to all data points.
        If an array-like, weights are applied element-wise.

    Returns
    -------
    histogram : uhi.numpy_plottable.PlottableHistogram
        The filled histogram object.

    Warns
    -----
    RangeWarning
        If more than 1% of the data is outside of the binning range.
    """
    if data is None:
        data = np.array([])

    if weights is None:
        weights = 1
    if isinstance(weights, (int, float)):
        weights = np.full_like(data, weights)

    hist, edges = np.histogram(data, bins=bins, range=range, weights=weights)

    # Check what proportion of the data is outside of the binning range
    range_coverage = np.sum(hist) / np.sum(np.asarray(weights))

    # Issue a warning if more than 1% of the data is outside of the binning range
    if range_coverage < 0.99:
        warnings.warn(
            f"Only {100 * range_coverage:.2f}% of data contained in the binning range [{edges[0]}, {edges[-1]}].",
            category=RangeWarning,
            stacklevel=2,
        )

    # compute variances
    variances = np.histogram(
        data, bins=bins, range=range, weights=np.array(weights) ** 2
    )[0]

    return EnhancedNumPyPlottableHistogram(hist, edges, variances=variances)


def make_2d_hist(data=None, bins=(10, 10), range=(None, None), weights=1):
    """
    Create a 2D histogram object and fill it with the provided data.

    Parameters
    ----------
    data : array-like, optional
        2D array-like data used to fill the histogram (default is None).
        If None is provided, an empty histogram is returned.
    bins : tuple, optional
        Binning specification for each dimension of the histogram (default is (10, 10)).
        Each element of the tuple represents the number of bins for the corresponding dimension.
        Also support explicit bin edges specification (for non-constant bin size).
    range : tuple, optional
        The range of values to consider for each dimension of the histogram (default is (None, None)).
        If None, the range is determined from the data for that dimension.
        The tuple should have the same length as the data.
    weights : float or array-like, optional
        Weight(s) to apply to the data points (default is 1).
        If a float, a single weight is applied to all data points.
        If an array-like, weights are applied element-wise.

    Returns
    -------
    histogram : EnhancedNumPyPlottableHistogram
        The filled 2D histogram object.

    Raises
    ------
    ValueError
        If the data does not have two components or if the lengths of x and y are not equal.

    Warns
    -----
    RangeWarning
        If more than 1% of the data is outside of the binning range.
    """
    if data is None:
        data = np.array([[], []])
    if len(data) != 2:
        raise ValueError("data should have two components, x and y")
    if len(data[0]) != len(data[1]):
        raise ValueError("x and y must have the same length.")

    if weights is None:
        weights = 1
    if isinstance(weights, (int, float)):
        weights = np.full_like(data[0], weights)

    hist, x_edges, y_edges = np.histogram2d(
        data[0], data[1], bins=bins, range=range, weights=weights
    )

    # Check what proportion of the data is outside of the binning range
    range_coverage = np.sum(hist) / np.sum(np.asarray(weights))

    # Issue a warning if more than 1% of the data is outside of the binning range
    if range_coverage < 0.99:
        warnings.warn(
            f"Only {100 * range_coverage:.2f}% of data contained in the binning range ([{x_edges[0]}, {x_edges[-1]}], [{y_edges[0]}, {y_edges[-1]}]).",
            category=RangeWarning,
            stacklevel=2,
        )

    # compute variances
    variances = np.histogram2d(
        data[0], data[1], bins=bins, range=range, weights=np.array(weights) ** 2
    )[0]

    return EnhancedNumPyPlottableHistogram(hist, x_edges, y_edges, variances=variances)


def _check_counting_histogram(hist):
    """
    Check that the histogram is a counting histogram.

    Parameters
    ----------
    hist : boost_histogram.Histogram
        The histogram to check.

    Raise
    -----
    ValueError
        If the histogram is not a counting histogram.

    """
    if hist.kind != Kind.COUNT:
        raise ValueError(
            f"The histogram must be a counting histogram, but the input histogram has kind {hist.kind}."
        )


def _make_hist_from_function(func, ref_hist):
    """
    Create a histogram from a function and a reference histogram.
    The returned histogram has the same binning as the reference histogram and
    is filled with the function evaluated at the bin centers of the reference histogram.

    Parameters
    ----------
    func : function
        1D function. The function should support vectorization (i.e. accept a numpy array as input).
    ref_hist : boost_histogram.Histogram
        The reference 1D histogram to use for the binning.

    Returns
    -------
    hist : boost_histogram.Histogram
        The histogram filled with the function.

    Raises
    ------
    ValueError
        If the reference histogram is not 1D.
    """
    if len(ref_hist.axes) != 1:
        raise ValueError("The reference histogram must be 1D.")

    return EnhancedNumPyPlottableHistogram(
        func(np.mean(ref_hist.axes[0].edges, axis=1)),
        ref_hist.axes[0].edges,
        variances=np.zeros_like(ref_hist.values()),
    )


def flatten_2d_hist(hist):
    """
    Flatten a 2D histogram into a 1D histogram.

    Parameters
    ----------
    hist : Histogram object
        The 2D histogram to be flattened.

    Returns
    -------
    Histogram object
        The flattened 1D histogram.

    Raises
    ------
    ValueError
        If the input histogram is not 2D.
    """
    _check_counting_histogram(hist)

    if len(hist.axes) != 2:
        raise ValueError("The input histogram must be 2D.")

    return EnhancedNumPyPlottableHistogram(
        hist.values().flatten(),
        variances=hist.variances().flatten(),
    )
