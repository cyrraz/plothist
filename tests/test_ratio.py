from plothist import make_hist, get_comparison
import numpy as np
from pytest import approx, raises


def test_ratio_weighted_histograms():
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
        get_comparison(h1w, h2, comparison="ratio", h1_uncertainty_type="asymmetrical")
    assert (
        str(err.value)
        == "Asymmetrical uncertainties can only be computed for an unweighted histogram."
    )


def test_ratio_simple_values():
    """
    Test ratio with simple values.
    """

    h1 = make_hist(data=[1] * 100, bins=1, range=(0, 3))
    h2 = make_hist(data=[1] * 10, bins=1, range=(0, 3))

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="ratio"
    )
    assert approx(values) == np.array([0.1])
    assert approx(high_uncertainty) == np.array([0.03316625])
    assert approx(low_uncertainty) == np.array([0.03316625])

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="ratio", h1_uncertainty_type="asymmetrical"
    )
    assert approx(values) == np.array([0.1])
    assert approx(high_uncertainty) == np.array([0.03265575])
    assert approx(low_uncertainty) == np.array([0.04382563])


def test_ratio_complex_values():
    """
    Test ratio with random values.
    """
    rng = np.random.default_rng(8311311)
    h1 = make_hist(data=rng.normal(size=100000), bins=10, range=(-5, 5))
    h2 = make_hist(data=rng.normal(size=80000), bins=10, range=(-5, 5))
    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="ratio"
    )
    print(list(values), "\n", list(high_uncertainty), "\n", list(low_uncertainty))

    assert approx(values) == np.array(
        [
            0.4,
            0.6618705035971223,
            0.7947897623400365,
            0.8067629291292177,
            0.7964303508103514,
            0.7981632533302037,
            0.8179000959197226,
            0.7402890695573623,
            0.9180327868852459,
            1.0,
        ]
    )
    assert approx(high_uncertainty) == np.array(
        [
            0.3346640106136302,
            0.08895650327968395,
            0.02553343623433043,
            0.010362621371283012,
            0.006475424104450652,
            0.006489300534544608,
            0.01047411689978261,
            0.02412251340854011,
            0.1201371137656762,
            1.0,
        ]
    )
    assert approx(high_uncertainty) == low_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="ratio", h1_uncertainty_type="asymmetrical"
    )

    assert approx(values) == np.array(
        [
            0.4,
            0.6618705035971223,
            0.7947897623400365,
            0.8067629291292177,
            0.7964303508103514,
            0.7981632533302037,
            0.8179000959197226,
            0.7402890695573623,
            0.9180327868852459,
            1.0,
        ]
    )
    assert approx(high_uncertainty) == np.array(
        [
            0.31424734572549723,
            0.08885909032232045,
            0.025532071318029308,
            0.010362534042899352,
            0.006475401990114839,
            0.006489278416967618,
            0.010474030233249552,
            0.024121102346281367,
            0.12004352597513421,
            0.9577036150850644,
        ]
    )
    assert approx(low_uncertainty) == np.array(
        [
            0.5570746229934151,
            0.09484770051247897,
            0.025879130731868948,
            0.010417720738564722,
            0.006497363933563098,
            0.006511254880705368,
            0.010529131460053793,
            0.024469519001226153,
            0.12637764392827852,
            1.4965212485612585,
        ]
    )
