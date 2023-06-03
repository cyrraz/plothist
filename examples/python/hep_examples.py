import matplotlib.pyplot as plt
from plothist.plotters import make_hist
from plothist.plotters import make_2d_hist
from plothist.plotters import cubehelix_palette
from plothist.hep_plotters import compare_data_mc
from plothist.hep_plotters import plot_b2_logo
from plothist.generate_dummy_data import generate_dummy_data

# Generate dummy data

df = generate_dummy_data()

# 1. Compare data and MC for a 1D variable
## 1.1 Define the histograms
key = "variable_1"
range = [-10, 10]
category = "category"

# Define masks

signal_mask = df[category] == 7
data_mask = df[category] == 8

background_categories = [0, 1, 2]  # [0, 1, 2, 3, 4, 5, 6]
background_categories_labels = [f"c{i}" for i in background_categories]
background_categories_colors = cubehelix_palette(
    ncolors=len(background_categories),
    start=1.5,
    rotation=1.5,
    darkest=0.3,
    lightest=0.8,
    reverse=True,
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

## 1.2 Compare data and stacked histogram
fig, ax_comparison, ax_ratio = compare_data_mc(
    data_hist=data_hist,
    mc_hist_list=background_hists,
    signal_hist=signal_hist,
    xlabel=key,
    ylabel="Entries",
    mc_labels=background_categories_labels,
    mc_colors=background_categories_colors,
    save_as=None,
    stacked=True,
)
plot_b2_logo(ax=ax_comparison)
## 1.3 Compare data and un-stacked histogram
fig, ax_comparison, ax_ratio = compare_data_mc(
    data_hist=data_hist,
    mc_hist_list=background_hists,
    signal_hist=None,
    xlabel=key,
    ylabel="Entries",
    mc_labels=background_categories_labels,
    mc_colors=background_categories_colors,
    save_as=None,
    stacked=False,
)

plot_b2_logo(ax=ax_comparison)
# 2 Compare data and stacked histogram for a flatten 2D variable
## 2.1 Define the histograms
key1 = "variable_1"
key2 = "variable_2"
# Bins [-10,0], [0,10] for variable 1,
# and bins [-10,-5], [-5,0], [0,5], [5,10] for variable 2
bins = [[-10,0,10],[-10,-5,0,5,10]]
category = "category"

# Define datasets

signal_mask = df[category] == 7
data_mask = df[category] == 8

background_categories = [0, 1, 2, 3, 4, 5, 6]
background_categories_labels = [f"c{i}" for i in background_categories]
background_categories_colors = cubehelix_palette(
    ncolors=len(background_categories),
    start=1.5,
    rotation=1.5,
    darkest=0.3,
    lightest=0.8,
    reverse=True,
)
background_masks = [df[category] == p for p in background_categories]

# Make histograms

data_hist = make_2d_hist(
    [df[key][data_mask] for key in [key1, key2]], bins=bins, weights=1
)
background_hists = [
    make_2d_hist(
        [df[key][mask] for key in [key1, key2]], bins=bins, weights=1
    )
    for mask in background_masks
]
signal_hist = make_2d_hist(
    [df[key][signal_mask] for key in [key1, key2]], bins=bins, weights=1
)

## 2.2 Compare data and stacked histogram
fig, ax_comparison, ax_ratio = compare_data_mc(
    data_hist=data_hist,
    mc_hist_list=background_hists,
    signal_hist=signal_hist,
    xlabel=rf"({key1} $\times$ {key2}) bin",
    ylabel="Entries",
    mc_labels=background_categories_labels,
    mc_colors=background_categories_colors,
    save_as=None,
    flatten_2d_hist=True,
)  # /!\ Important argument

plot_b2_logo(ax=ax_comparison)
ax_comparison.legend(ncol=3, fontsize=10)

plt.show()
