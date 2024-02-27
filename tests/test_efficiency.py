from plothist import make_hist, get_comparison
import numpy as np
from pytest import approx, raises


def test_efficiency_subsample():
    """
    Test subsample error.
    """
    h1 = make_hist(data=np.random.normal(size=11), bins=100, range=(-5, 5))
    h2 = make_hist(data=np.random.normal(size=10), bins=100, range=(-5, 5))
    with raises(ValueError) as err:
        get_comparison(h1, h2, comparison="efficiency")
    assert (
        str(err.value)
        == "The ratio of two correlated histograms (efficiency) can only be computed if the bin contents of h1 are a subsample of the bin contents of h2."
    )


def test_efficiency_weighted_histograms():
    """
    Test weighted histograms error.
    """
    h1 = make_hist(data=np.random.normal(size=10), bins=10, range=(-5, 5))
    h2 = make_hist(data=np.random.normal(size=100), bins=10, range=(-5, 5))
    h1w = make_hist(
        data=np.random.normal(size=10),
        bins=10,
        range=(-5, 5),
        weights=np.random.normal(size=10),
    )
    h2w = make_hist(
        data=np.random.normal(size=100),
        bins=10,
        range=(-5, 5),
        weights=np.random.normal(size=100),
    )

    error_msg = "The ratio of two correlated histograms (efficiency) can only be computed for unweighted histograms."

    with raises(ValueError) as err:
        get_comparison(h1w, h2, comparison="efficiency")
    assert str(err.value) == error_msg

    with raises(ValueError) as err:
        get_comparison(h1, h2w, comparison="efficiency")
    assert str(err.value) == error_msg

    with raises(ValueError) as err:
        get_comparison(h1w, h2w, comparison="efficiency")
    assert str(err.value) == error_msg


def simple_efficiency_uncertainty(total, sample):
    """
    Calculate the uncertainty of the efficiency of a sample, derived from the Binomial Statistics.
    """
    efficiency = sample / total
    return np.sqrt(efficiency * (1 - efficiency) / total)


def test_efficiency_simple_values():
    """
    Test efficiency with simple values.
    """
    n1 = 100
    n2 = 10

    h1 = make_hist(data=[1] * n1, bins=1, range=(0, 2))
    h2 = make_hist(data=[1] * n2, bins=1, range=(0, 2))

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="efficiency"
    )
    assert approx(values) == np.array([0.1])
    assert approx(high_uncertainty) == np.array([0.03056316])
    assert approx(low_uncertainty) == np.array([0.03056316])

    assert approx(high_uncertainty[0], 0.02) == simple_efficiency_uncertainty(
        n1, n2
    )  # 0.02 relative error
    assert approx(low_uncertainty[0], 0.02) == simple_efficiency_uncertainty(
        n1, n2
    )  # 0.02 relative error

    # Test with larger numbers
    n1 = 10000000
    n2 = 1000000

    h1 = make_hist(data=[1] * n1, bins=1, range=(0, 2))
    h2 = make_hist(data=[1] * n2, bins=1, range=(0, 2))

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="efficiency"
    )

    assert approx(values) == np.array([0.1])
    assert approx(high_uncertainty) == np.array([9.48683493e-05])
    assert approx(low_uncertainty) == np.array([9.48683493e-05])

    assert approx(high_uncertainty[0]) == simple_efficiency_uncertainty(
        n1, n2
    )  # 1e-6 relative error by default
    assert approx(low_uncertainty[0]) == simple_efficiency_uncertainty(
        n1, n2
    )  # 1e-6 relative error by default


def test_efficiency_complex_values():
    """
    Test efficiency with random values.
    """
    rng = np.random.default_rng(8311311)
    x1 = rng.normal(size=100000)
    x2 = rng.choice(x1, size=10000)
    h1 = make_hist(data=x1, bins=10, range=(-5, 5))
    h2 = make_hist(data=x2, bins=10, range=(-5, 5))
    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="efficiency"
    )

    assert approx(values) == np.array(
        [
            0.0,
            0.1079136690647482,
            0.09734917733089579,
            0.09864446736407839,
            0.10128659769643328,
            0.09779355671615515,
            0.10337194717036818,
            0.10388437217705511,
            0.10655737704918032,
            0.0,
        ]
    )
    assert approx(high_uncertainty) == np.array(
        [
            0.12371791482634838,
            0.02661654698726243,
            0.006343589231090674,
            0.0025597549707911415,
            0.0016334320872715157,
            0.0016090633836174837,
            0.002615474280842884,
            0.006489834814808297,
            0.02830633673352296,
            0.19364916731037085,
        ]
    )
    assert approx(low_uncertainty) == np.array(
        [
            0.12371791482634838,
            0.02661654698726243,
            0.006343589231090674,
            0.0025597549707911415,
            0.0016334320872715157,
            0.0016090633836174837,
            0.002615474280842884,
            0.006489834814808297,
            0.02830633673352296,
            0.19364916731037085,
        ]
    )
    assert approx(high_uncertainty) == low_uncertainty
