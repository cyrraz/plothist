from plothist import make_hist, get_comparison
import numpy as np
from pytest import approx


def test_efficiency_subsample():
    """
    Test subsample error.
    """
    h1 = make_hist(data=np.random.normal(size=11), bins=100, range=(-5, 5))
    h2 = make_hist(data=np.random.normal(size=10), bins=100, range=(-5, 5))
    try:
        get_comparison(h1, h2, comparison="efficiency")
        assert False
    except ValueError:
        assert True


def test_efficiency_simple_values():
    """
    Test efficiency with simple values.
    """
    h1 = make_hist(data=[1] * 100, bins=1, range=(0, 2))
    h2 = make_hist(data=[1] * 10, bins=1, range=(0, 2))

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="efficiency"
    )
    assert approx(values) == np.array([0.1])
    assert approx(high_uncertainty) == np.array([0.03056316])
    assert approx(low_uncertainty) == np.array([0.03056316])


def test_efficiency_complex_values():
    """
    Test efficiency with random values.
    """
    np.random.seed(8311311)
    x1 = np.random.normal(size=100000)
    # Sample a subset of x1
    x2 = np.random.choice(x1, size=10000)
    h1 = make_hist(data=x1, bins=10, range=(-5, 5))
    h2 = make_hist(data=x2, bins=10, range=(-5, 5))
    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="efficiency"
    )
    assert approx(values) == np.array(
        [
            0.0,
            0.11194029850746269,
            0.08786610878661087,
            0.10043157047765343,
            0.10032448377581121,
            0.1001991681799543,
            0.10057009209179944,
            0.09644670050761421,
            0.10666666666666667,
            0.0,
        ]
    )
    assert approx(high_uncertainty) == np.array(
        [
            0.19364916731037085,
            0.02752652713580867,
            0.006111813184158927,
            0.0025710863669062846,
            0.0016318216468728468,
            0.0016251250652707272,
            0.0025716247924324667,
            0.0063480077226947835,
            0.025480153593469827,
            0.23570226039551584,
        ]
    )
    assert approx(low_uncertainty) == np.array(
        [
            0.19364916731037085,
            0.02752652713580867,
            0.006111813184158927,
            0.0025710863669062846,
            0.0016318216468728468,
            0.0016251250652707272,
            0.0025716247924324667,
            0.0063480077226947835,
            0.025480153593469827,
            0.23570226039551584,
        ]
    )
