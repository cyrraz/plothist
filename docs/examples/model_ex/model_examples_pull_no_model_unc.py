"""
Pull plot, no model uncertainty
===============================

This example shows how to plot a pull plot with data/model comparison without model uncertainty.
"""

from plothist.get_dummy_data import get_dummy_data

df = get_dummy_data()

from plothist import make_hist, get_color_palette

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
background_scaling_factor = data_hist.sum().value / sum(background_hists).sum().value
background_hists = [background_scaling_factor * h for h in background_hists]

signal_scaling_factor = data_hist.sum().value / signal_hist.sum().value
signal_hist *= signal_scaling_factor

###
from plothist import plot_data_model_comparison, add_luminosity

fig, ax_main, ax_comparison = plot_data_model_comparison(
    data_hist=data_hist,
    stacked_components=background_hists,
    stacked_labels=background_categories_labels,
    stacked_colors=background_categories_colors,
    xlabel=f"${key}\,\,[eV/c^2]$",
    ylabel="Hits in the LMN per $4.2\\times 10^{-1}\,\,eV/c^2$",
    comparison="pull",
    model_uncertainty=False,  # <--
)
add_luminosity(
    collaboration="Beast III", ax=ax_main, lumi=8.2, lumi_unit="zb", preliminary=True
)

fig.savefig("model_examples_pull_no_model_unc.svg", bbox_inches="tight")
