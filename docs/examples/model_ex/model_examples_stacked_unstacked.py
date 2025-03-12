"""
Data vs model with stacked and unstacked components
===================================================

Plot data and a model with stacked and unstacked components.
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
from plothist import plot_data_model_comparison

fig, ax_main, ax_comparison = plot_data_model_comparison(
    data_hist=data_hist,
    stacked_components=background_hists[:2],
    stacked_labels=background_categories_labels[:2],
    stacked_colors=background_categories_colors[:2],
    unstacked_components=background_hists[2:],
    unstacked_labels=background_categories_labels[2:],
    unstacked_colors=background_categories_colors[2:],
    xlabel=key,
    ylabel="Entries",
    model_sum_kwargs={"show": True, "label": "Model", "color": "navy"},
    comparison_ylim=(0.5, 1.5),
)

fig.savefig("model_examples_stacked_unstacked.svg", bbox_inches="tight")
