"""Test cases for different histogram input types."""

import boost_histogram as bh
import hist
import matplotlib
import matplotlib.gridspec as gridspec
import numpy as np
import pytest
import uproot
from matplotlib.testing.decorators import check_figures_equal
from plothist_utils import get_dummy_data

from plothist import get_color_palette, make_hist, plot_data_model_comparison, plot_hist
from plothist.histogramming import make_plottable_histogram

matplotlib.use("agg")


@pytest.fixture
def sample_data():
    """
    Pytest fixture that returns a dummy DataFrame to be reused across multiple tests.
    """
    return get_dummy_data()


@check_figures_equal(extensions=["png"])
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

    # convert to plottable histogram
    h_numpy = make_plottable_histogram(h_numpy)

    ax_test = fig_test.subplots()
    plot_hist(h_numpy, ax=ax_test)


@check_figures_equal(extensions=["png"])
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
    h_boost_histogram = bh.Histogram(
        bh.axis.Regular(5, min(sample_data[name]), max(sample_data[name]))
    )
    h_boost_histogram.fill(sample_data[name])

    # convert to plottable histogram
    h_boost_histogram = make_plottable_histogram(h_boost_histogram)

    ax_test = fig_test.subplots()
    plot_hist(h_boost_histogram, ax=ax_test)


@check_figures_equal(extensions=["png"])
def test_hist_input(fig_test, fig_ref, sample_data):
    """
    Test Hist input.
    """

    name = "variable_0"

    # === Reference Figure ===
    h = make_hist(sample_data[name], bins=5)
    ax_ref = fig_ref.subplots()
    plot_hist(h, ax=ax_ref)

    # === Test Figure ===
    h_hist = hist.Hist.new.Reg(
        5, sample_data[name].min(), sample_data[name].max()
    ).Double()
    h_hist.fill(sample_data[name])

    # convert to plottable histogram
    h_hist = make_plottable_histogram(h_hist)

    ax_test = fig_test.subplots()
    plot_hist(h_hist, ax=ax_test)


ROOT = pytest.importorskip("ROOT")


@check_figures_equal(extensions=["png"])
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

    # convert to plottable histogram
    h_root = make_plottable_histogram(h_root)

    ax_test = fig_test.subplots()
    plot_hist(h_root, ax=ax_test)


@check_figures_equal(extensions=["png"])
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

    # convert to plottable histogram
    h_uproot = make_plottable_histogram(h_uproot)

    ax_test = fig_test.subplots()
    plot_hist(h_uproot, ax=ax_test)


def test_data_model_comparison_simple_run(sample_data):
    df = sample_data

    # Define the histograms

    key = "variable_1"
    range_ = [-9, 12]
    category = "category"
    bins = 50

    # Define masks
    data_mask = df[category] == 8

    background_categories = [0, 1, 2, 3, 4]
    background_categories_labels = [
        "ROOT",
        "Uproot",
        "Hist",
        "boost_histogram",
        "NumPy",
    ]
    background_categories_colors = get_color_palette(
        "cubehelix", len(background_categories)
    )

    background_masks = {
        label: df[category] == p
        for p, label in zip(background_categories, background_categories_labels)
    }

    # Make histograms

    # Data histogram
    arbitrary_factor_for_a_nicer_figure = 4
    h_data = make_hist(
        np.repeat(df[key][data_mask], arbitrary_factor_for_a_nicer_figure),
        bins=bins,
        range=range_,
        weights=1,
    )

    # ROOT
    h_root = ROOT.TH1F("h", "h", bins, range_[0], range_[1])
    for val in df[key][background_masks["ROOT"]]:
        h_root.Fill(val)

    # Uproot
    h_uproot = ROOT.TH1F("h", "h", bins, range_[0], range_[1])
    h_uproot.SetDirectory(0)  # Prevent ROOT from tracking this object globally
    for val in df[key][background_masks["Uproot"]]:
        h_uproot.Fill(val)
    h_uproot = uproot.pyroot.from_pyroot(h_uproot)

    # Hist
    h_hist = hist.Hist.new.Reg(bins, range_[0], range_[1]).Double()
    h_hist.fill(df[key][background_masks["Hist"]])

    # boost_histogram
    h_boost_histogram = bh.Histogram(bh.axis.Regular(bins, range_[0], range_[1]))
    h_boost_histogram.fill(df[key][background_masks["boost_histogram"]])

    # NumPy
    h_numpy = np.histogram(
        df[key][background_masks["NumPy"]],
        bins=bins,
        range=range_,
    )

    background_hists = {
        "ROOT": h_root,
        "Uproot": h_uproot,
        "Hist": h_hist,
        "boost_histogram": h_boost_histogram,
        "NumPy": h_numpy,
    }

    fig, _, _ = plot_data_model_comparison(
        data_hist=h_data,
        stacked_components=[background_hists[k] for k in background_categories_labels],
        stacked_labels=background_categories_labels,
        stacked_colors=background_categories_colors,
        xlabel="Dummy variable",
        ylabel="Entries",
        comparison="pull",
        comparison_ylim=(-20, 20),
    )

    fig.savefig("test_data_model_comparison_diverse_inputs.pdf", bbox_inches="tight")


@check_figures_equal(extensions=["png"])
def test_data_model_comparison_figure_equal(fig_test, fig_ref, sample_data):
    df = sample_data

    # Define the histograms

    key = "variable_1"
    range_ = [-9, 12]
    category = "category"

    # Define masks
    data_mask = df[category] == 8

    background_categories = [0, 1, 2]
    background_categories_labels = [f"c{i}" for i in background_categories]
    background_categories_colors = get_color_palette(
        "cubehelix", len(background_categories)
    )

    background_masks = [df[category] == p for p in background_categories]

    # Make histograms
    data_hist = make_hist(df[key][data_mask], bins=50, range=range_, weights=1)
    background_hists = [
        make_hist(df[key][mask], bins=50, range=range_, weights=1)
        for mask in background_masks
    ]

    gs_ref = gridspec.GridSpec(2, 1, figure=fig_ref, height_ratios=[4, 1])
    gs_test = gridspec.GridSpec(2, 1, figure=fig_test, height_ratios=[4, 1])

    axes_ref = []
    axes_test = []

    for i in range(2):
        axes_ref.append(fig_ref.add_subplot(gs_ref[i]))
        axes_test.append(fig_test.add_subplot(gs_test[i]))

    fig_ref, _, _ = plot_data_model_comparison(
        data_hist=data_hist,
        stacked_components=background_hists,
        stacked_labels=background_categories_labels,
        stacked_colors=background_categories_colors,
        xlabel=f"${key}\,\,[TeV/c^2]$",
        ylabel="Candidates per 0.42 $TeV/c^2$",
        comparison="pull",
        fig=fig_ref,
        ax_main=axes_ref[0],
        ax_comparison=axes_ref[1],
    )
    fig_test, _, _ = plot_data_model_comparison(
        data_hist=data_hist,
        stacked_components=background_hists,
        stacked_labels=background_categories_labels,
        stacked_colors=background_categories_colors,
        xlabel=f"${key}\,\,[TeV/c^2]$",
        ylabel="Candidates per 0.42 $TeV/c^2$",
        comparison="pull",
        fig=fig_test,
        ax_main=axes_test[0],
        ax_comparison=axes_test[1],
    )

    fig_ref.tight_layout()
    fig_test.tight_layout()
