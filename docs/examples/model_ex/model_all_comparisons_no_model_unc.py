"""
Data/model comparisons, no model uncertainty
============================================

All supported comparisons between data and model, without model uncertainty.
"""

from plothist import get_dummy_data

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
from plothist import (
    create_comparison_figure,
    plot_data_model_comparison,
    add_text,
    set_fitting_ylabel_fontsize,
    plot_comparison,
)
import numpy as np

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
    model_uncertainty=False,  # <--
    comparison="ratio",
    fig=fig,
    ax_main=axes[0],
    ax_comparison=axes[1],
)

add_text(
    "Multiple data-model comparisons, $\mathbf{without}$ model uncertainty",
    ax=axes[0],
)
add_text('  $\mathbf{→}$ comparison = "ratio"', ax=axes[1], fontsize=13)

for k_comp, comparison in enumerate(
    ["split_ratio", "pull", "relative_difference", "difference"], start=2
):
    ax_comparison = axes[k_comp]

    # Copy the original histogram and set the uncertainties of the copy to 0.
    background_sum_copy = background_sum.copy()
    background_sum_copy[:] = np.c_[
        background_sum_copy.values(), np.zeros_like(background_sum_copy.values())
    ]

    plot_comparison(
        data_hist,
        background_sum_copy,
        ax=ax_comparison,
        comparison=comparison,
        xlabel="",
        h1_label="Data",
        h2_label="Pred.",
        h1_uncertainty_type="asymmetrical",
    )
    if comparison == "pull":
        # Since the uncertainties of the model are neglected, the pull label is "(Data - Pred.)/sigma_Data"
        ax_comparison.set_ylabel(r"$\frac{Data-Pred.}{\sigma_{Data}}$")
    add_text(
        f'  $\mathbf{{→}}$ comparison = "{comparison}"', ax=ax_comparison, fontsize=13
    )
    set_fitting_ylabel_fontsize(ax_comparison)

axes[-1].set_xlabel(key)

fig.savefig("model_all_comparisons_no_model_unc.svg", bbox_inches="tight")
