"""
Model with stacked and unstacked histograms components
======================================================

This example shows how to plot a model made of stacked and unstacked histograms components.
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
from plothist import plot_model, add_luminosity, add_text

fig, ax = plot_model(
    stacked_components=background_hists,
    stacked_labels=background_categories_labels,
    stacked_colors=background_categories_colors,
    unstacked_components=[signal_hist],
    unstacked_labels=["Signal"],
    unstacked_colors=["black"],
    unstacked_kwargs_list=[{"linestyle": "dotted"}],
    xlabel=key,
    ylabel="Entries",
    model_sum_kwargs={"show": True, "label": "Model", "color": "navy"},
    model_uncertainty_label="Stat. unc.",
)

add_text("Model made of histograms", ax=ax)

add_luminosity(collaboration="Beast III", ax=ax, preliminary=True, is_data=False)

fig.savefig(
    "model_with_stacked_and_unstacked_histograms_components.svg", bbox_inches="tight"
)
