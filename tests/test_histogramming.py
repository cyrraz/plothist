import boost_histogram as bh
import numpy as np
from plothist import make_hist, make_2d_hist
from pytest import warns
from plothist.histogramming import EnhancedNumPyPlottableHistogram
from uhi.numpy_plottable import NumPyPlottableAxis


def test_make_hist():
    """
    Test make_hist() function.
    """
    h = make_hist(data=[0, 1, 2, 3, 4], bins=5, range=(0, 5))
    assert isinstance(h, EnhancedNumPyPlottableHistogram)
    assert isinstance(h.axes[0], NumPyPlottableAxis)
    assert h.values().sum() == 5
    assert h.variances().sum() == 5
    assert h.values()[0] == 1
    assert h.values()[0] == 1


def test_upper_edge_inclusive():
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


def test_upper_edge_exclusive():
    """
    Check that upper edge of last bin is exclusive when overflow=True.
    """

    data = [0] * 3 + [1] * 4 + [2] * 5 + [3] * 6 + [4] * 7 + [5] * 8

    a1 = bh.axis.Regular(5, 0, 5, overflow=True)
    a2 = bh.axis.Variable([0, 1, 2, 3, 4, 5], overflow=True)
    a3 = bh.axis.Regular(5, min(data), max(data), overflow=True)
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


def test_histogram_addition():
    """
    Test adding two histograms.
    """
    h1 = make_hist(data=[0, 1, 2, 3, 4], bins=5, range=(0, 5))
    h2 = make_hist(data=[0, 1, 2, 3, 4], bins=5, range=(0, 5))
    h3 = h1 + h2
    assert np.array_equal((h1 + h2).values(), [2, 2, 2, 2, 2])
    assert np.array_equal(sum([h1, h2, h3]).values(), [4, 4, 4, 4, 4])


def test_histogram_multiplication():
    """
    Test multiplying a histogram by a scalar.
    """
    h1 = make_hist(data=[0, 1, 2, 3, 4], bins=5, range=(0, 5), weights=2)
    h2 = 2 * h1
    h3 = h1 * 2
    assert np.array_equal(h2.values(), [4, 4, 4, 4, 4])
    assert np.array_equal(h2.variances(), [16, 16, 16, 16, 16])
    assert np.array_equal(h3.values(), [4, 4, 4, 4, 4])
    assert np.array_equal(h3.variances(), [16, 16, 16, 16, 16])


def test_range_coverage_warning():

    warn_message = r"Only 80.00% of data contained in the binning range [0.0, 5.0]."

    with warns(Warning) as warn_info:
        _ = make_hist(data=[0, 1, 2, 3, 10], bins=5, range=(0, 5))
    assert str(warn_info[0].message) == warn_message

    with warns(Warning) as warn_info:
        _ = make_hist(data=[0, 1, 2, 3, 10], bins=5, range=(0, 5), weights=2)
    assert str(warn_info[0].message) == warn_message

    with warns(Warning) as warn_info:
        _ = make_hist(data=[0, 1, 2, 3, 10], bins=5, range=(0, 5), weights=[2] * 5)
    assert str(warn_info[0].message) == warn_message

    warn_message_2d = (
        r"Only 80.00% of data contained in the binning range ([0.0, 5.0], [0.0, 5.0])."
    )

    with warns(Warning) as warn_info:
        _ = make_2d_hist(
            data=[[0, 1, 2, 3, 10], [0, 1, 2, 3, 10]],
            bins=(5, 5),
            range=((0, 5), (0, 5)),
        )
    assert str(warn_info[0].message) == warn_message_2d

    with warns(Warning) as warn_info:
        _ = make_2d_hist(
            data=[[0, 1, 2, 3, 10], [0, 1, 2, 3, 10]],
            bins=(5, 5),
            range=((0, 5), (0, 5)),
            weights=2,
        )
    assert str(warn_info[0].message) == warn_message_2d

    with warns(Warning) as warn_info:
        _ = make_2d_hist(
            data=[[0, 1, 2, 3, 10], [0, 1, 2, 3, 10]],
            bins=(5, 5),
            range=((0, 5), (0, 5)),
            weights=[2] * 5,
        )
    assert str(warn_info[0].message) == warn_message_2d
