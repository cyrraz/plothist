import boost_histogram as bh
import pytest

from plothist.comparison import (
    _check_binning_consistency,
    _check_uncertainty_type,
    get_comparison,
)


def test_check_uncertainty_type_invalid():
    with pytest.raises(
        ValueError,
        match="Uncertainty type invalid_type not valid. Must be 'symmetrical' or 'asymmetrical'.",
    ):
        _check_uncertainty_type("invalid_type")


def test_check_binning_consistency_dimensionality():
    h1 = bh.Histogram(bh.axis.Regular(10, 0, 1))
    h2 = bh.Histogram(bh.axis.Regular(10, 0, 1), bh.axis.Regular(5, 0, 5))
    with pytest.raises(ValueError, match="Histograms must have same dimensionality."):
        _check_binning_consistency([h1, h2])


def test_check_binning_consistency_bins():
    h1 = bh.Histogram(bh.axis.Regular(10, 0, 1))
    h2 = bh.Histogram(bh.axis.Regular(5, 0, 1))
    with pytest.raises(ValueError, match="The bins of the histograms must be equal."):
        _check_binning_consistency([h1, h2])


def test_invalid_comparison_type():
    h1 = bh.Histogram(bh.axis.Regular(10, 0, 1))
    h2 = bh.Histogram(bh.axis.Regular(10, 0, 1))
    with pytest.raises(ValueError, match="invalid not available as a comparison"):
        get_comparison(h1, h2, comparison="invalid")
