from __future__ import annotations

import warnings
from collections.abc import Sequence
from typing import Callable

import boost_histogram as bh
import numpy as np


# Define a custom warning for range issues
class RangeWarning(Warning):
    pass


# Always show the range warnings
warnings.filterwarnings("always", category=RangeWarning)


def create_axis(
    bins: int | list[float] | np.ndarray,
    range: tuple[float | str, float | str] | None = None,
    data: list[float] | np.ndarray | None = None,
    overflow: bool = False,
    underflow: bool = False,
) -> bh.axis.Regular | bh.axis.Variable:
    """
    Create an axis object for histogram binning based on the input data and parameters.

    Parameters
    ----------
    bins : int or list[float]
        The number of bins or bin edges for the axis.
    range : None or tuple[float | str, float | str], optional
        The range of the axis. If None, it will be determined based on the data. Default is None.
    data : list[float] or np.ndarray, optional
        The input data for determining the axis range. Default is None.
    overflow : bool, optional
        Whether to include an overflow bin. If False, the upper edge of the last bin is inclusive. Default is False.
    underflow : bool, optional
        Whether to include an underflow bin. Default is False.

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
        If the number of bins is not positive.
    ValueError
        If the range parameter contains "min" or "max" but the data is empty.
    """
    if data is None:
        data = np.array([])

    is_variable_bins = isinstance(bins, (list, np.ndarray))

    if is_variable_bins:
        if range is not None:
            warnings.warn(
                f"Custom binning -> ignore supplied range ({range}).", stacklevel=2
            )
        return bh.axis.Variable(bins, underflow=underflow, overflow=overflow)

    if isinstance(bins, int) and bins <= 0:
        raise ValueError(f"Number of bins must be positive, but got {bins}.")

    # Inspired from np.histograms
    if range is not None:
        if len(data) == 0 and (range[0] == "min" or range[1] == "max"):
            raise ValueError(
                "Cannot use 'min'/'max' range values with empty data. "
                "Please supply a range or provide data."
            )
        x_min = min(data) if range[0] == "min" else float(range[0])
        x_max = max(data) if range[1] == "max" else float(range[1])
        if x_min > x_max:
            raise ValueError(
                f"Range of [{x_min}, {x_max}] is not valid. Max must be larger than min."
            )
        if not (np.isfinite(x_min) and np.isfinite(x_max)):
            raise ValueError(f"Range of [{x_min}, {x_max}] is not finite.")
    elif len(data) == 0:
        # handle empty arrays. Can't determine range, so use 0-1.
        x_min, x_max = 0.0, 1.0
    else:
        x_min = float(min(data))
        x_max = float(max(data))
        if not (np.isfinite(x_min) and np.isfinite(x_max)):
            raise ValueError(f"Autodetected range of [{x_min}, {x_max}] is not finite.")

    # expand empty range to avoid divide by zero
    if x_min == x_max:
        x_min = x_min - 0.5
        x_max = x_max + 0.5

    return bh.axis.Regular(bins, x_min, x_max, underflow=underflow, overflow=overflow)


def make_hist(
    data: list[float] | np.ndarray | None = None,
    bins: int | list[float] | np.ndarray = 50,
    range: tuple[float | str, float | str] | None = None,
    weights: float | list[float] | np.ndarray = 1,
) -> bh.Histogram:
    """
    Create a histogram object and fill it with the provided data.

    Parameters
    ----------
    data : list[float] or np.ndarray, optional
        1D array-like data used to fill the histogram (default is None).
        If None is provided, an empty histogram is returned.
    bins : int or list[float], optional
        Binning specification for the histogram (default is 50).
        If an integer, it represents the number of bins.
        If a list, it should be the explicit list of all bin edges.
    range : tuple[float | str, float | str], optional
        The range of values to consider for the histogram bins (default is None).
        If None, the range is determined from the data.
    weights : float or list[float] or np.ndarray, optional
        Weight(s) to apply to the data points (default is 1).
        If a float, a single weight is applied to all data points.
        If an array-like, weights are applied element-wise.

    Returns
    -------
    histogram : bh.Histogram
        The filled histogram object.

    Warns
    -----
    RangeWarning
        If more than 1% of the data is outside of the binning range.
    """
    if data is None:
        data = np.array([])

    axis = create_axis(bins, range, data)

    h = bh.Histogram(axis, storage=bh.storage.Weight())

    if len(data) > 0:
        h.fill(data, weight=weights, threads=0)

        # Check what proportion of the data outside of the binning range
        n_data = (
            len(data) * weights
            if isinstance(weights, (int, float))
            else np.sum(np.asarray(weights))
        )

        range_coverage = h.sum().value / n_data

        # Issue a warning if more than 1% of the data is outside of the binning range
        if range_coverage < 0.99:
            warnings.warn(
                f"Only {100 * range_coverage:.2f}% of data contained in the binning range [{axis.edges[0]}, {axis.edges[-1]}].",
                category=RangeWarning,
                stacklevel=2,
            )

    return h


def make_2d_hist(
    data: list[np.ndarray] | np.ndarray | None = None,
    bins: Sequence[int | Sequence[float]] | None = None,
    range: tuple[
        tuple[float | str, float | str] | None, tuple[float | str, float | str] | None
    ] = (None, None),
    weights: float | list[float] | np.ndarray = 1,
) -> bh.Histogram:
    """
    Create a 2D histogram object and fill it with the provided data.

    Parameters
    ----------
    data : list[np.ndarray] or np.ndarray, optional
        2D array-like data used to fill the histogram (default is None).
        If None is provided, an empty histogram is returned.
    bins : Sequence[int | Sequence[float]], optional
        Binning specification for each dimension of the histogram (if None, it will be set to [10, 10]).
        Each element of the tuple represents the number of bins for the corresponding dimension.
        Also support explicit bin edges specification (for non-constant bin size).
    range : tuple[tuple[float | str, float | str] | None, tuple[float | str, float | str] | None], optional
        The range of values to consider for each dimension of the histogram (default is (None, None)).
        If None, the range is determined from the data for that dimension.
        The tuple should have the same length as the data.
    weights : float or list[float] or np.ndarray, optional
        Weight(s) to apply to the data points (default is 1).
        If a float, a single weight is applied to all data points.
        If an array-like, weights are applied element-wise.

    Returns
    -------
    histogram : bh.Histogram
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
    if bins is None:
        bins = [10, 10]

    x_axis = create_axis(bins[0], range[0], data[0])
    y_axis = create_axis(bins[1], range[1], data[1])

    h = bh.Histogram(
        x_axis,
        y_axis,
        storage=bh.storage.Weight(),
    )

    if len(data[0]) > 0:
        h.fill(*data, weight=weights, threads=0)

        # Check what proportion of the data outside of the binning range
        n_data = (
            len(data[0]) * weights
            if isinstance(weights, (int, float))
            else np.sum(np.asarray(weights))
        )

        range_coverage = h.sum().value / n_data

        # Issue a warning if more than 1% of the data is outside of the binning range
        if range_coverage < 0.99:
            warnings.warn(
                f"Only {100 * range_coverage:.2f}% of data contained in the binning range ([{x_axis.edges[0]}, {x_axis.edges[-1]}], [{y_axis.edges[0]}, {y_axis.edges[-1]}]).",
                category=RangeWarning,
                stacklevel=2,
            )

    return h


def _check_counting_histogram(hist: bh.Histogram) -> None:
    """
    Check that the histogram is a counting histogram.

    Parameters
    ----------
    hist : bh.Histogram
        The histogram to check.

    Raise
    -----
    ValueError
        If the histogram is not a counting histogram.

    """
    if hist.kind != bh.Kind.COUNT:
        raise ValueError(
            f"The histogram must be a counting histogram, but the input histogram has kind {hist.kind}."
        )


def _make_hist_from_function(
    func: Callable[[np.ndarray], np.ndarray], ref_hist: bh.Histogram
) -> bh.Histogram:
    """
    Create a histogram from a function and a reference histogram.
    The returned histogram has the same binning as the reference histogram and
    is filled with the function evaluated at the bin centers of the reference histogram.

    Parameters
    ----------
    func : Callable[[np.ndarray], np.ndarray]
        1D function. The function should support vectorization (i.e. accept a numpy array as input).
    ref_hist : bh.Histogram
        The reference 1D histogram to use for the binning.

    Returns
    -------
    hist : bh.Histogram
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


def flatten_2d_hist(hist: bh.Histogram) -> bh.Histogram:
    """
    Flatten a 2D histogram into a 1D histogram.

    Parameters
    ----------
    hist : bh.Histogram
        The 2D histogram to be flattened.

    Returns
    -------
    bh.Histogram
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
