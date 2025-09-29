from __future__ import annotations

import boost_histogram as bh
import numpy as np
import pytest

from plothist import create_axis, make_2d_hist, make_hist
from plothist.histogramming import (
    _check_counting_histogram,
    _make_hist_from_function,
    flatten_2d_hist,
)


def test_make_hist() -> None:
    """
    Test make_hist() function.
    """
    h = make_hist(data=[0, 1, 2, 3, 4], bins=5, range=(0, 5))
    assert isinstance(h, bh.Histogram)
    assert isinstance(h.axes[0], bh.axis.Regular)
    assert h.sum().value == 5
    assert h.sum().variance == 5
    assert h[0].value == 1
    assert h[-1].value == 1


def test_upper_edge_inclusive() -> None:
    """
    Check that upper edge of last bin is inclusive by default.
    This comes from the fact that make_hist() turns off the underflow and overflow bins by default.
    """

    data = [0] * 3 + [1] * 4 + [2] * 5 + [3] * 6 + [4] * 7 + [5] * 8
    h1 = make_hist(data=data * 2, bins=5, range=(0, 5))
    h2 = make_hist(data=data * 2, bins=[0, 1, 2, 3, 4, 5])
    h3 = make_hist(data=data, bins=[0, 1, 2, 3, 4, 5], weights=2)
    h4 = make_hist(data=data, bins=[0, 1, 2, 3, 4, 5], weights=[2] * len(data))

    expected = [6, 8, 10, 12, 30]

    for h in [h1, h2, h3, h4]:
        assert np.array_equal(h.values(), expected)


def test_upper_edge_exclusive() -> None:
    """
    Check that upper edge of last bin is exclusive when overflow=True.
    """

    data = [0] * 3 + [1] * 4 + [2] * 5 + [3] * 6 + [4] * 7 + [5] * 8

    a1 = create_axis(5, (0, 5), overflow=True)
    a2 = create_axis([0, 1, 2, 3, 4, 5], overflow=True)
    a3 = create_axis(5, data=data, overflow=True)
    # For a integer axis, the last bin is always exclusive, no matter the overflow setting.
    int_a1 = bh.axis.Integer(0, 5, overflow=False)
    int_a2 = bh.axis.Integer(0, 5, overflow=True)

    h1 = bh.Histogram(a1, storage=bh.storage.Weight())
    h2 = bh.Histogram(a2, storage=bh.storage.Weight())
    h3 = bh.Histogram(a3, storage=bh.storage.Weight())
    h4 = bh.Histogram(int_a1, storage=bh.storage.Weight())
    h5 = bh.Histogram(int_a2, storage=bh.storage.Weight())
    h6 = h1.copy()
    h7 = h2.copy()
    h8 = h3.copy()
    h9 = h4.copy()
    h10 = h5.copy()

    h1.fill(data * 2)
    h2.fill(data * 2)
    h3.fill(data * 2)
    h4.fill(data * 2)
    h5.fill(data * 2)
    h6.fill(data, weight=[2] * len(data))
    h7.fill(data, weight=[2] * len(data))
    h8.fill(data, weight=[2] * len(data))
    h9.fill(data, weight=[2] * len(data))
    h10.fill(data, weight=[2] * len(data))

    expected = [6, 8, 10, 12, 14]

    for h in [h1, h2, h3, h4, h5, h6, h7, h8, h9, h10]:
        assert np.array_equal(h.values(), expected)


def test_range_coverage_warning() -> None:
    """
    Test that a warning is raised when to much data is outside the binning range.
    """
    warn_message = r"Only 80.00% of data contained in the binning range [0.0, 5.0]."

    with pytest.warns(Warning) as warn_info:
        _ = make_hist(data=[0, 1, 2, 3, 10], bins=5, range=(0, 5))
    assert str(warn_info[0].message) == warn_message

    with pytest.warns(Warning) as warn_info:
        _ = make_hist(data=[0, 1, 2, 3, 10], bins=5, range=(0, 5), mute_warning=True)
    assert str(warn_info[0].message) == ""

    with pytest.warns(Warning) as warn_info:
        _ = make_hist(data=[0, 1, 2, 3, 10], bins=5, range=(0, 5), weights=2)
    assert str(warn_info[0].message) == warn_message

    with pytest.warns(Warning) as warn_info:
        _ = make_hist(data=[0, 1, 2, 3, 10], bins=5, range=(0, 5), weights=[2] * 5)
    assert str(warn_info[0].message) == warn_message

    warn_message_2d = (
        r"Only 80.00% of data contained in the binning range ([0.0, 5.0], [0.0, 5.0])."
    )

    with pytest.warns(Warning) as warn_info:
        _ = make_2d_hist(
            data=[[0, 1, 2, 3, 10], [0, 1, 2, 3, 10]],
            bins=(5, 5),
            range=((0, 5), (0, 5)),
        )
    assert str(warn_info[0].message) == warn_message_2d

    with pytest.warns(Warning) as warn_info:
        _ = make_2d_hist(
            data=[[0, 1, 2, 3, 10], [0, 1, 2, 3, 10]],
            bins=(5, 5),
            range=((0, 5), (0, 5)),
            weights=2,
        )
    assert str(warn_info[0].message) == warn_message_2d

    with pytest.warns(Warning) as warn_info:
        _ = make_2d_hist(
            data=[[0, 1, 2, 3, 10], [0, 1, 2, 3, 10]],
            bins=(5, 5),
            range=((0, 5), (0, 5)),
            weights=[2] * 5,
        )
    assert str(warn_info[0].message) == warn_message_2d


def test_warning_when_range_is_provided_with_variable_bins() -> None:
    """Test for the warning when range is provided with variable bins."""
    bins = [1, 2, 3, 4]
    range_value = (0, 5)

    with pytest.warns(Warning, match="Custom binning -> ignore supplied range"):
        create_axis(bins=bins, range=range_value)


def test_invalid_bins() -> None:
    """Test for non-positive bins."""
    with pytest.raises(
        ValueError, match="Number of bins must be positive, but got -5."
    ):
        create_axis(bins=-5)

    with pytest.raises(ValueError, match="Number of bins must be positive, but got 0."):
        create_axis(bins=0)


def test_range_min_max_with_empty_data() -> None:
    """Test for using 'min' or 'max' in range with empty data."""
    with pytest.raises(
        ValueError,
        match="Cannot use 'min'/'max' range values with empty data. "
        "Please supply a range or provide data.",
    ):
        create_axis(bins=5, range=("min", "max"), data=[])


def test_invalid_range_values() -> None:
    """Test for invalid range (non-finite values)."""
    with pytest.raises(ValueError, match=r"Range of \[nan, 10.0\] is not finite."):
        create_axis(bins=5, range=(np.nan, 10.0))

    with pytest.raises(ValueError, match=r"Range of \[0.0, inf\] is not finite."):
        create_axis(bins=5, range=(0.0, np.inf))


def test_range_min_greater_than_max() -> None:
    """Test for case where min > max in range."""
    with pytest.raises(
        ValueError,
        match=r"Range of \[10.0, 5.0\] is not valid. Max must be larger than min.",
    ):
        create_axis(bins=5, range=(10.0, 5.0))


def test_autodetect_range_invalid() -> None:
    """Test for non-finite autodetected range."""
    with pytest.raises(
        ValueError, match=r"Autodetected range of \[nan, nan\] is not finite."
    ):
        create_axis(bins=5, data=[np.nan, 10.0])

    with pytest.raises(
        ValueError, match=r"Autodetected range of \[0.0, inf\] is not finite."
    ):
        create_axis(bins=5, data=[0.0, np.inf])


def test_auto_range_for_empty_data() -> None:
    """Test that auto range is correctly set for empty data."""
    axis = create_axis(10, data=[])
    assert isinstance(axis, bh.axis.Regular)
    assert axis.edges[0] == 0.0 and axis.edges[-1] == 1.0


def test_range_expansion_when_min_equals_max() -> None:
    """Test that range is expanded when min equals max in data."""
    axis = create_axis(10, data=[2.0, 2.0])
    assert isinstance(axis, bh.axis.Regular)
    assert axis.edges[0] == 1.5 and axis.edges[-1] == 2.5


def test_make_hist_with_empty_data() -> None:
    """
    Test make_hist() with empty data.
    """
    h = make_hist(data=None, bins=5, range=(0, 5))
    assert h.values().sum() == 0
    assert h.variances().sum() == 0


def test_make_2d_hist_with_empty_data() -> None:
    """
    Test make_2d_hist() with empty data.
    """
    h = make_2d_hist(data=None, bins=(5, 5), range=((0, 5), (0, 5)))
    assert h.values().sum() == 0


def test_make_make_2d_hist_with_invalid_data_dimensions() -> None:
    """
    Test make_hist() with invalid data dimensions.
    """
    with pytest.raises(ValueError, match="data should have two components, x and y"):
        make_2d_hist(data=[1, 2, 3], bins=5, range=(0, 5))


def test_make_2d_hist_with_different_x_y_lengths() -> None:
    """
    Test make_2d_hist() with different lengths of x and y data.
    """
    with pytest.raises(ValueError, match="x and y must have the same length"):
        make_2d_hist(data=[[1, 2, 3], [4, 5]], bins=(5, 5), range=((0, 5), (0, 5)))


def test_check_counting_histogram_invalid() -> None:
    """Test that _check_counting_histogram raises ValueError for non-counting histogram."""
    hist = bh.Histogram(bh.axis.Regular(10, 0, 1), storage=bh.storage.Mean())
    with pytest.raises(ValueError, match="The histogram must be a counting histogram"):
        _check_counting_histogram(hist)


def test_make_hist_from_function_raises_on_non_1d_hist() -> None:
    """Test that _make_hist_from_function raises ValueError if ref_hist is not 1D."""
    hist_2d = make_2d_hist()

    def func(x):
        return x**2

    with pytest.raises(ValueError, match="The reference histogram must be 1D."):
        _make_hist_from_function(func, hist_2d)


def test_flatten_2d_hist_raises_on_1d_hist() -> None:
    """Test that flatten_2d_hist raises ValueError if the input histogram is not 2D."""
    hist_1d = make_hist()
    with pytest.raises(ValueError, match="The input histogram must be 2D."):
        flatten_2d_hist(hist_1d)
