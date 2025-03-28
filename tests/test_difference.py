import numpy as np
from pytest import approx, raises

from plothist import get_comparison, make_hist


def test_difference_weighted_histograms():
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
        get_comparison(
            h1w, h2, comparison="difference", h1_uncertainty_type="asymmetrical"
        )
    assert (
        str(err.value)
        == "Asymmetrical uncertainties can only be computed for an unweighted histogram."
    )


def test_difference_simple_values():
    """
    Test difference with simple values.
    """

    h1 = make_hist(data=[1] * 50, bins=1, range=(0, 3))
    h2 = make_hist(data=[1] * 100, bins=1, range=(0, 3))

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="difference"
    )
    assert approx(values) == np.array([50.0])
    assert approx(high_uncertainty) == np.array([12.24744871391589])
    assert approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="difference", h1_uncertainty_type="asymmetrical"
    )
    assert approx(values) == np.array([50.0])
    assert approx(high_uncertainty) == np.array([12.233780151938355])
    assert approx(low_uncertainty) == np.array([13.104772168594577])


def test_difference_complex_values():
    """
    Test difference with random values.
    """
    rng = np.random.default_rng(8311311)
    h1 = make_hist(data=rng.normal(size=100000), bins=10, range=(-5, 5))
    h2 = make_hist(data=rng.normal(size=80000), bins=10, range=(-5, 5))
    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="difference"
    )

    assert approx(values) == np.array(
        [-3.0, -47.0, -449.0, -2623.0, -6946.0, -6879.0, -2468.0, -575.0, -10.0, 0.0]
    )
    assert approx(high_uncertainty) == np.array(
        [
            2.6457513110645907,
            15.198684153570664,
            62.66578013557319,
            156.60459763365824,
            247.58029000710053,
            247.55807399476996,
            156.96496424361712,
            62.07253821135398,
            15.297058540778355,
            2.0,
        ]
    )
    assert approx(high_uncertainty) == low_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="difference", h1_uncertainty_type="asymmetrical"
    )

    assert approx(values) == np.array(
        [-3.0, -47.0, -449.0, -2623.0, -6946.0, -6879.0, -2468.0, -575.0, -10.0, 0.0]
    )
    assert approx(high_uncertainty) == np.array(
        [
            2.5823990507642316,
            15.187670343763216,
            62.66311771237798,
            156.60353291251036,
            247.5796166128547,
            247.55740054015223,
            156.96390196934192,
            62.069850261501465,
            15.28611912206896,
            1.9154072301701288,
        ]
    )
    assert approx(low_uncertainty) == np.array(
        [
            3.458077990673633,
            15.87202875900091,
            63.34102670156633,
            157.2767218220309,
            248.24860043264547,
            248.22678627397232,
            157.63960095483972,
            62.73478020967331,
            16.02801576337975,
            2.993042497122517,
        ]
    )
