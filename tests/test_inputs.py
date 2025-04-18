import boost_histogram as bh
import matplotlib
import numpy as np
import pytest
import uproot
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


@check_figures_equal()
def test_boost_histogram_input(fig_test, fig_ref, sample_data):
    """
    Test Boost histogram input.
    """

    name = "variable_0"

    # === Reference Figure ===
    h = make_hist(sample_data[name], bins=5)
    ax_ref = fig_ref.subplots()
    plot_hist(h, ax=ax_ref)

    # === Test Figure ===
    hist = bh.Histogram(
        bh.axis.Regular(5, min(sample_data[name]), max(sample_data[name]))
    )
    hist.fill(sample_data[name])
    ax_test = fig_test.subplots()
    plot_hist(hist, ax=ax_test, flow="none")  # do not show flow bins


# This is failing
# @check_figures_equal()
# def test_hist_input(fig_test, fig_ref, sample_data):
#     """
#     Test Hist input.
#     """

#     name = "variable_0"

#     # === Reference Figure ===
#     h = make_hist(sample_data[name], bins=5)
#     ax_ref = fig_ref.subplots()
#     plot_hist(h, ax=ax_ref)

#     # === Test Figure ===
#     hist_obj = hist.Hist.new.Reg(
#         5, sample_data[name].min(), sample_data[name].max()
#     ).Double()
#     hist_obj.fill(sample_data[name])
#     ax_test = fig_test.subplots()
#     plot_hist(hist_obj, ax=ax_test, flow="none")  # do not show flow bins


ROOT = pytest.importorskip("ROOT")


@check_figures_equal()
def test_root_histogram_input(fig_test, fig_ref, sample_data):
    """
    Test ROOT histogram input.
    """

    name = "variable_0"

    # === Reference Figure ===
    h = make_hist(sample_data[name], bins=5)
    ax_ref = fig_ref.subplots()
    plot_hist(h, ax=ax_ref)

    # === Test Figure ===
    h_root = ROOT.TH1F("h", "h", 5, min(sample_data[name]), max(sample_data[name]))
    for val in sample_data[name]:
        h_root.Fill(val)
    ax_test = fig_test.subplots()
    plot_hist(h_root, ax=ax_test)


@check_figures_equal()
def test_pyroot_to_uproot_histogram_input(fig_test, fig_ref, sample_data):
    """
    Test ROOT histogram input with PyROOT to Uproot conversion.
    """

    name = "variable_0"

    # === Reference Figure ===
    h = make_hist(sample_data[name], bins=5)
    ax_ref = fig_ref.subplots()
    plot_hist(h, ax=ax_ref)

    # === Test Figure ===
    h_root = ROOT.TH1F("h", "h", 5, min(sample_data[name]), max(sample_data[name]))
    h_root.SetDirectory(0)  # Prevent ROOT from tracking this object globally
    for val in sample_data[name]:
        h_root.Fill(val)
    h_uproot = uproot.pyroot.from_pyroot(h_root)
    ax_test = fig_test.subplots()
    plot_hist(h_uproot, ax=ax_test, flow="none")  # do not show flow bins
