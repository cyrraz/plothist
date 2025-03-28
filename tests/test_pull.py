import numpy as np
from pytest import approx, raises

from plothist import get_comparison, make_hist


def test_pull_weighted_histograms():
    """
    Test weighted histograms error.
    """
    h1w = make_hist(
        data=np.random.normal(size=10),
        bins=10,
        range=(-5, 5),
        weights=np.random.normal(size=10),
    )
    h2 = make_hist(data=np.random.normal(size=10), bins=10, range=(-5, 5))

    with raises(ValueError) as err:
        get_comparison(h1w, h2, comparison="pull", h1_uncertainty_type="asymmetrical")
    assert (
        str(err.value)
        == "Asymmetrical uncertainties can only be computed for an unweighted histogram."
    )


def test_pull_simple_values():
    """
    Test pull with simple values.
    """

    h1 = make_hist(data=[1] * 100, bins=1, range=(0, 3))
    h2 = make_hist(data=[1] * 50, bins=1, range=(0, 3))

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="pull"
    )
    assert approx(values) == np.array([-4.08248290463863])
    assert approx(high_uncertainty) == np.array([1.0])
    assert approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="pull", h1_uncertainty_type="asymmetrical"
    )
    assert approx(values) == np.array([-3.8818568847803108])
    assert approx(high_uncertainty) == np.array([1.0])
    assert approx(low_uncertainty) == high_uncertainty


def test_pull_complex_values():
    """
    Test pull with random values.
    """
    rng = np.random.default_rng(8311311)
    h1 = make_hist(data=rng.normal(size=100000), bins=10, range=(-5, 5))
    h2 = make_hist(data=rng.normal(size=80000), bins=10, range=(-5, 5))
    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="pull"
    )

    assert approx(values) == np.array(
        [
            -1.1338934190276817,
            -3.092372966310914,
            -7.164994978577123,
            -16.749188974233867,
            -28.055545131645136,
            -27.787419287101617,
            -15.723253987874301,
            -9.263355689470163,
            -0.6537204504606134,
            0.0,
        ]
    )
    assert approx(high_uncertainty) == np.array([1.0] * 10)
    assert approx(high_uncertainty) == low_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="pull", h1_uncertainty_type="asymmetrical"
    )

    assert approx(values) == np.array(
        [
            -0.867533933037641,
            -2.9611841506616883,
            -7.088612600415852,
            -16.677611089631554,
            -27.980016756970926,
            -27.71256117543868,
            -15.655964523197618,
            -9.16556969002242,
            -0.6239075471118297,
            0.0,
        ]
    )
    assert approx(high_uncertainty) == np.array([1.0] * 10)
    assert approx(high_uncertainty) == low_uncertainty
