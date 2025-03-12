"""
Flatten 2D histograms
=====================

This example shows how to flatten and display 2D histograms on one dimension.
"""

from plothist import get_dummy_data

df = get_dummy_data()

from plothist import make_hist, get_color_palette
from uhi.numpy_plottable import NumPyPlottableHistogram

# Define the histograms

key = "variable_1"
range = [-9, 12]
category = "category"

# Define masks
signal_mask = df[category] == 7
data_mask = df[category] == 8

background_categories = [0, 1, 2]
background_categories_labels = [f"c{i}" for i in background_categories]
background_categories_colors = get_color_palette(
    "cubehelix", len(background_categories)
)

background_masks = [df[category] == p for p in background_categories]

# Make histograms
data_hist = make_hist(df[key][data_mask], bins=50, range=range, weights=1)
background_hists = [
    make_hist(df[key][mask], bins=50, range=range, weights=1)
    for mask in background_masks
]
signal_hist = make_hist(df[key][signal_mask], bins=50, range=range, weights=1)

# Optional: scale to data
background_scaling_factor = data_hist.values().sum() / sum(
    h.values().sum() for h in background_hists
)
background_hists = [
    NumPyPlottableHistogram(
        h.values() * background_scaling_factor,
        h.axes[0].edges,
        variances=h.variances() * background_scaling_factor**2,
    )
    for h in background_hists
]

signal_scaling_factor = data_hist.values().sum() / signal_hist.values().sum()
signal_hist = NumPyPlottableHistogram(
    signal_hist.values() * signal_scaling_factor,
    signal_hist.axes[0].edges,
    variances=signal_hist.variances() * signal_scaling_factor**2,
)

###
from plothist import (
    make_2d_hist,
    get_color_palette,
    plot_data_model_comparison,
    flatten_2d_hist,
    plot_hist,
)

# Define the histograms

key1 = "variable_1"
key2 = "variable_2"
# Bins [-10,0], [0,10] for variable 1,
# and bins [-10,-5], [-5,0], [0,5], [5,10] for variable 2
bins = [[-10, 0, 10], [-10, -5, 0, 5, 10]]
category = "category"

# Define datasets

signal_mask = df[category] == 7
data_mask = df[category] == 8

background_categories = [0, 1, 2, 3, 4, 5, 6]
background_categories_labels = [f"c{i}" for i in background_categories]
background_categories_colors = get_color_palette(
    "cubehelix", len(background_categories)
)

background_masks = [df[category] == p for p in background_categories]

# Make histograms

data_hist = make_2d_hist(
    [df[key][data_mask] for key in [key1, key2]], bins=bins, weights=1
)
background_hists = [
    make_2d_hist([df[key][mask] for key in [key1, key2]], bins=bins, weights=1)
    for mask in background_masks
]
signal_hist = make_2d_hist(
    [df[key][signal_mask] for key in [key1, key2]], bins=bins, weights=1
)

# Flatten the 2D histograms
data_hist = flatten_2d_hist(data_hist)
background_hists = [flatten_2d_hist(h) for h in background_hists]
signal_hist = flatten_2d_hist(signal_hist)

# Compare data and stacked histogram
fig, ax_main, ax_comparison = plot_data_model_comparison(
    data_hist=data_hist,
    stacked_components=background_hists,
    stacked_labels=background_categories_labels,
    stacked_colors=background_categories_colors,
    xlabel=rf"({key1} $\times$ {key2}) bin",
    ylabel="Entries",
)

plot_hist(
    signal_hist,
    ax=ax_main,
    color="red",
    label="Signal",
    histtype="step",
)

ax_main.legend(ncol=3, fontsize=10, loc="upper left")

fig.savefig("model_examples_flatten2D.svg", bbox_inches="tight")
