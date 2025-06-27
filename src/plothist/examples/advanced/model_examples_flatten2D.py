"""
Flatten 2D histograms
=====================

This example shows how to flatten and display 2D histograms on one dimension.
"""

from plothist_utils import get_dummy_data

df = get_dummy_data()

###
from plothist import (
    flatten_2d_hist,
    get_color_palette,
    make_2d_hist,
    plot_data_model_comparison,
    plot_hist,
)

# Define the histograms

key1 = "variable_1"
key2 = "variable_2"
# Bins [-12,0], [0,12] for variable 1,
# and bins [-12,-5], [-5,0], [0,5], [5,12] for variable 2
bins = [[-12, 0, 12], [-12, -5, 0, 5, 12]]
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
    xlabel=rf"({key1} $\times$ {key2}) bin number",
    ylabel="Entries",
)

plot_hist(
    signal_hist,
    ax=ax_main,
    color="red",
    label="Signal",
    histtype="step",
)

for ax in [ax_main, ax_comparison]:
    ax.set_xticks([i + 0.5 for i in range(8)])
    ax.tick_params(axis="x", which="minor", bottom=False)
ax_comparison.set_xticklabels([str(i + 1) for i in range(8)])

ax_main.legend(ncol=3, fontsize=10, loc="upper left")

fig.savefig("model_examples_flatten2D.svg", bbox_inches="tight")
