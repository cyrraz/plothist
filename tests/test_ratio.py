from __future__ import annotations

import numpy as np
from pytest import approx, raises

from plothist import get_comparison, make_hist


def test_ratio_weighted_histograms() -> None:
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


def test_ratio_simple_values() -> None:
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
    assert approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="ratio", h1_uncertainty_type="asymmetrical"
    )
    assert approx(values) == np.array([0.1])
    assert approx(high_uncertainty) == np.array([0.03265575])
    assert approx(low_uncertainty) == np.array([0.04382563])


def test_ratio_complex_values() -> None:
    """
    Test ratio with random values.
    """
    rng = np.random.default_rng(8311311)
    h1 = make_hist(data=rng.normal(size=100000), bins=10, range=(-5, 5))
    h2 = make_hist(data=rng.normal(size=80000), bins=10, range=(-5, 5))
    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="ratio"
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


def test_split_ratio_simple_values() -> None:
    """
    Test split ratio with simple values.
    """

    h1 = make_hist(data=[1] * 100, bins=1, range=(0, 3))
    h2 = make_hist(data=[1] * 10, bins=1, range=(0, 3))

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="split_ratio"
    )
    assert approx(values) == np.array([0.1])
    assert approx(high_uncertainty) == np.array([0.0316227766016838])
    assert approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="split_ratio", h1_uncertainty_type="asymmetrical"
    )
    assert approx(values) == np.array([0.1])
    assert approx(high_uncertainty) == np.array([0.031086944386636207])
    assert approx(low_uncertainty) == np.array([0.04266949759891313])


def test_split_ratio_complex_values() -> None:
    """
    Test split ratio with random values.
    """
    rng = np.random.default_rng(8311311)
    h1 = make_hist(data=rng.normal(size=100000), bins=10, range=(-5, 5))
    h2 = make_hist(data=rng.normal(size=80000), bins=10, range=(-5, 5))
    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="split_ratio"
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
            0.282842712474619,
            0.06900477011960747,
            0.019059103712973532,
            0.007709372753648256,
            0.004831289095230075,
            0.004839308721902339,
            0.007768414861135622,
            0.01828571136404441,
            0.08674594462506854,
            0.7071067811865476,
        ]
    )
    assert approx(high_uncertainty) == low_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="split_ratio", h1_uncertainty_type="asymmetrical"
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
            0.2583629119969045,
            0.06887914601983501,
            0.019057275098979868,
            0.007709255370032222,
            0.00483125945512883,
            0.004839279063162287,
            0.007768298008664885,
            0.018283849850174488,
            0.0866162856135678,
            0.6459072799922612,
        ]
    )
    assert approx(low_uncertainty) == np.array(
        [
            0.5275719245593493,
            0.07644923227878979,
            0.019519797023699485,
            0.007783277712946144,
            0.004860655827597242,
            0.00486870902804312,
            0.007842432908702224,
            0.01874110314510096,
            0.09520105928933346,
            1.3189298113983732,
        ]
    )
