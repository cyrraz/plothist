import boost_histogram as bh
import numpy as np
from plothist import make_hist, make_2d_hist
from plothist import create_axis
from pytest import warns


def test_make_hist():
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
