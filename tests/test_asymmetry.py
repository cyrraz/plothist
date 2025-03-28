import numpy as np
from pytest import approx

from plothist import get_comparison, make_hist


def test_asymmetry_simple_values():
    """
    Test asymmetry with simple values.
    """

    h1 = make_hist(data=[1] * 50, bins=1, range=(0, 3))
    h2 = make_hist(data=[1] * 100, bins=1, range=(0, 3))

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="asymmetry"
    )
    assert approx(values) == np.array([0.3333333333333333])
    assert approx(high_uncertainty) == np.array([0.08606629658238704])
    assert approx(low_uncertainty) == high_uncertainty


def test_asymmetry_complex_values():
    """
    Test asymmetry with random values.
    """
    rng = np.random.default_rng(8311311)
    h1 = make_hist(data=rng.normal(size=100000), bins=10, range=(-5, 5))
    h2 = make_hist(data=rng.normal(size=80000), bins=10, range=(-5, 5))
    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="asymmetry"
    )

    assert approx(values) == np.array(
        [
            -0.42857142857142855,
            -0.20346320346320346,
            -0.11433664374840845,
            -0.10695208970438329,
            -0.11331897676846776,
            -0.11224606347393326,
            -0.10017046838217387,
            -0.1492343628341552,
            -0.042735042735042736,
            0.0,
        ]
    )
    assert approx(high_uncertainty) == np.array(
        [
            0.41121309550224255,
            0.06714322983291869,
            0.016061640147033433,
            0.006421925838700013,
            0.004064944404444152,
            0.004064823476588014,
            0.0064027316127981,
            0.01628859006719069,
            0.06543171177234845,
            0.5,
        ]
    )
    assert approx(high_uncertainty) == low_uncertainty
