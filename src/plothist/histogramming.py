import boost_histogram as bh
import numpy as np

import warnings


def create_axis(bins, range=None, data=np.array([])):
    """
    Create an axis object for histogram binning based on the input data and parameters.

    Parameters
    ----------
    bins : int or array-like
        The number of bins or bin edges for the axis.
    range : None or tuple, optional
        The range of the axis. If None, it will be determined based on the data.
    data : array-like, optional
        The input data for determining the axis range. Default is an empty array.

    Returns
    -------
    Axis object
        An axis object for histogram binning.
        The axis type is determined based on the input parameters.
        If bins is an integer, a regular axis is returned.
        If bins is an array-like, a variable axis is returned.

    Raises
    ------
    ValueError
        If the range parameter is invalid or not finite.
    ValueError
        If the range parameter contains "min" or "max" but the data is empty.
    """

    try:
        N = len(bins)
    except TypeError:
        N = 1

    if N > 1:
        if range is not None:
            warnings.warn(f"Custom binning -> ignore supplied range ({range}).")
        return bh.axis.Variable(bins)

    # Inspired from np.histograms
    if range is not None:
        if len(data) == 0 and (range[0] == "min" or range[1] == "max"):
            raise ValueError(
                "Cannot use 'min'/'max' range values with empty data. "
                "Please supply a range or provide data."
            )
        x_min = min(data) if range[0] == "min" else range[0]
        x_max = max(data) if range[1] == "max" else range[1]
        if x_min > x_max:
            raise ValueError(
                f"Range of [{x_min}, {x_max}] is not valid. Max must be larger than min."
            )
        if not (np.isfinite(x_min) and np.isfinite(x_max)):
            raise ValueError(f"Range of [{x_min}, {x_max}] is not finite.")
    elif len(data) == 0:
        # handle empty arrays. Can't determine range, so use 0-1.
        x_min, x_max = 0, 1
    else:
        x_min, x_max = min(data), max(data)
        if not (np.isfinite(x_min) and np.isfinite(x_max)):
            raise ValueError(f"Autodetected range of [{x_min}, {x_max}] is not finite.")

    # expand empty range to avoid divide by zero
    if x_min == x_max:
        x_min = x_min - 0.5
        x_max = x_max + 0.5

    return bh.axis.Regular(bins, x_min, x_max)


def make_hist(data=np.array([]), bins=50, range=None, weights=1):
    """
    Create a histogram object and fill it with the provided data.

    Parameters
    ----------
    data : array-like, optional
        1D array-like data used to fill the histogram (default is an empty array).
        If an empty array, an empty histogram is returned.
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
    histogram : boost_histogram.Histogram
        The filled histogram object.
    """

    axis = create_axis(bins, range, data)

    h = bh.Histogram(axis, storage=bh.storage.Weight())

    if len(data) > 0:
        h.fill(data, weight=weights, threads=0)

        # Check what proportion of the data is in the underflow and overflow bins
        range_coverage = h.values().sum() / h.values(flow=True).sum()
        # Issue a warning in more than 1% of the data is outside of the binning range
        if range_coverage < 0.99:
            warnings.warn(
                f"Only {100*range_coverage:.2f}% of data contained in the binning range [{axis.edges[0]}, {axis.edges[-1]}). Note that the upper edge is exclusive."
            )

    return h


def make_2d_hist(data=np.array([[], []]), bins=(10, 10), range=(None, None), weights=1):
    """
    Create a 2D histogram object and fill it with the provided data.

    Parameters
    ----------
    data : array-like, optional
        2D array-like data used to fill the histogram (default is an empty array).
        If an empty array, an empty histogram is returned.
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
    histogram : boost_histogram.Histogram
        The filled 2D histogram object.

    Raises
    ------
    ValueError
        If the data does not have two components or if the lengths of x and y are not equal.
    """
    if len(data) != 2:
        raise ValueError("data should have two components, x and y")
    if len(data[0]) != len(data[1]):
        raise ValueError("x and y must have the same length.")

    x_axis = create_axis(bins[0], range[0], data[0])
    y_axis = create_axis(bins[1], range[1], data[1])

    h = bh.Histogram(
        x_axis,
        y_axis,
        storage=bh.storage.Weight(),
    )

    if len(data[0]) > 0:
        h.fill(*data, weight=weights, threads=0)

        # Check what proportion of the data is in the underflow and overflow bins
        range_coverage = h.values().sum() / h.values(flow=True).sum()
        # Issue a warning in more than 1% of the data is outside of the binning range
        if range_coverage < 0.99:
            warnings.warn(
                f"Only {100*range_coverage:.2f}% of data contained in the binning range ([{x_axis.edges[0]}, {x_axis.edges[-1]}), [{y_axis.edges[0]}, {y_axis.edges[-1]})). Note that the upper edges are exclusive."
            )

    return h


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
    kind = hist.kind
    if kind != bh.Kind.COUNT:
        raise ValueError(
            f"The histogram must be a counting histogram, but the input histogram has kind {kind}."
        )
    return


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

    hist = bh.Histogram(ref_hist.axes[0], storage=bh.storage.Weight())
    hist[:] = np.c_[
        func(ref_hist.axes[0].centers), np.zeros_like(ref_hist.axes[0].centers)
    ]
    return hist


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
    n_bins = hist.axes[0].size * hist.axes[1].size
    flatten_hist = bh.Histogram(
        bh.axis.Regular(n_bins, 0, n_bins), storage=bh.storage.Weight()
    )
    flatten_hist[:] = np.c_[hist.values().flatten(), hist.variances().flatten()]
    return flatten_hist
