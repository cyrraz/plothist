"""
Data/model comparisons
======================

All supported comparisons between data and model.
"""

from plothist_utils import get_dummy_data

df = get_dummy_data()

from plothist import get_color_palette, make_hist

# Define the histograms

key = "variable_1"
range = (-9, 12)
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

# Optional: scale to data
background_scaling_factor = data_hist.sum().value / sum(background_hists).sum().value
background_hists = [background_scaling_factor * h for h in background_hists]

###
from plothist import (
    add_text,
    create_comparison_figure,
    plot_comparison,
    plot_data_model_comparison,
    set_fitting_ylabel_fontsize,
)

fig, axes = create_comparison_figure(
    figsize=(6, 13),
    nrows=6,
    gridspec_kw={"height_ratios": [3, 1, 1, 1, 1, 1]},
    hspace=0.3,
)
background_sum = sum(background_hists)

plot_data_model_comparison(
    data_hist=data_hist,
    stacked_components=background_hists,
    stacked_labels=background_categories_labels,
    stacked_colors=background_categories_colors,
    xlabel="",
    ylabel="Entries",
    comparison="ratio",
    fig=fig,
    ax_main=axes[0],
    ax_comparison=axes[1],
)

add_text(
    r"Multiple data-model comparisons, $\mathbf{with}$ model uncertainty",
    ax=axes[0],
)
add_text(r'  $\mathbf{→}$ comparison = "ratio"', ax=axes[1], fontsize=13)

for k_comp, comparison in enumerate(
    ["split_ratio", "pull", "relative_difference", "difference"], start=2
):
    ax_comparison = axes[k_comp]

    plot_comparison(
        data_hist,
        background_sum,
        ax=ax_comparison,
        comparison=comparison,
        xlabel="",
        h1_label="Data",
        h2_label="Pred.",
        h1_uncertainty_type="asymmetrical",
    )
    add_text(
        rf'  $\mathbf{{→}}$ comparison = "{comparison}"',
        ax=ax_comparison,
        fontsize=13,
    )
    set_fitting_ylabel_fontsize(ax_comparison)

axes[-1].set_xlabel(key)

fig.savefig("model_all_comparisons.svg", bbox_inches="tight")
