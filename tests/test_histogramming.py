from plothist import make_hist
import boost_histogram as bh


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
