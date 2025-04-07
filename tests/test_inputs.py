import matplotlib
import numpy as np
import pytest
from matplotlib.testing.decorators import check_figures_equal
from plothist_utils import get_dummy_data

from plothist import make_hist, plot_hist

matplotlib.use("agg")


@pytest.fixture
def sample_data():
    """
    Pytest fixture that returns a dummy DataFrame to be reused across multiple tests.
    """
    return get_dummy_data()


@check_figures_equal()
def test_numpy_histogram_input(fig_test, fig_ref, sample_data):
    """
    Test numpy histogram input.
    """

    name = "variable_0"

    # === Reference Figure ===
    h = make_hist(sample_data[name], bins=5)
    h._variances = np.zeros_like(
        h.variances()
    )  # Set variances to zero because numpy histogram does not have variances
    ax_ref = fig_ref.subplots()
    plot_hist(h, ax=ax_ref)

    # === Test Figure ===
    h_numpy = np.histogram(sample_data[name], bins=5)
    ax_test = fig_test.subplots()
    plot_hist(h_numpy, ax=ax_test)
