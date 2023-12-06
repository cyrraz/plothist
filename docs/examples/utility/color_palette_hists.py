"""
Color palette presentation
==========================

Create a plot with 4 color palettes displayed.
"""

from plothist import get_dummy_data

df = get_dummy_data()

import matplotlib.pyplot as plt
from plothist import make_hist, get_color_palette, add_text, plot_model, plot_error_hist

# Define the histograms
key = "variable_1"
xrange = [-8, 10]
category = "category"

# Define masks
signal_mask = df[category] == 7
data_mask = df[category] == 8

background_categories = [0, 1, 2, 3, 4, 5]
background_categories_labels = [f"c{i}" for i in background_categories]
background_masks = [df[category] == p for p in background_categories]

# Make histograms
data_hist = make_hist(df[key][data_mask], bins=50, range=xrange, weights=1)
background_hists = [
    make_hist(df[key][mask], bins=50, range=xrange, weights=1)
    for mask in background_masks
]
signal_hist = make_hist(df[key][signal_mask], bins=50, range=xrange, weights=1)

# Optional: scale to data
background_scaling_factor = data_hist.sum().value / sum(background_hists).sum().value
background_hists = [background_scaling_factor * h for h in background_hists]

signal_scaling_factor = data_hist.sum().value / signal_hist.sum().value
signal_hist *= signal_scaling_factor


# Plotting section
nrows, ncols = 2, 2

fig, axes = plt.subplots(
    nrows=nrows,
    ncols=ncols,
    figsize=(12, 10),
)
fig.subplots_adjust(hspace=0.25)

cmap_list = ["viridis", "ggplot", "coolwarm", "YlGnBu_r"]
ax_coords = [(x, y) for x in range(nrows) for y in range(ncols)]

for k, cmap_name in enumerate(cmap_list):
    background_categories_colors = get_color_palette(
        cmap_name, len(background_categories)
    )

    ax = axes[ax_coords[k]]

    plot_model(
        stacked_components=background_hists,
        stacked_labels=background_categories_labels,
        stacked_colors=background_categories_colors,
        xlabel=key,
        ylabel="Entries",
        model_uncertainty=False,
        fig=fig,
        ax=ax,
    )

    plot_error_hist(
        data_hist,
        color="black",
        label="Data",
        ax=ax,
    )

    ax.set_xlim(xrange)
    ax.legend()

    cmap_name = cmap_name.replace("_", "\_")
    add_text(
        f"$\mathrm{{\mathbf{{cmap = {cmap_name}}}}}$", x="right", fontsize=12, ax=ax
    )

fig.savefig(
    "usage_colorpalette_examples.svg",
    bbox_inches="tight",
)
