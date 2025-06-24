"""
Pull plot, no model uncertainty
===============================

Compare data and model with pulls, without model uncertainty.
"""

from plothist_utils import get_dummy_data

df = get_dummy_data()

from plothist import get_color_palette, make_hist

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

# Optional: scale to data
background_scaling_factor = data_hist.sum().value / sum(background_hists).sum().value
background_hists = [background_scaling_factor * h for h in background_hists]

###
from plothist import add_luminosity, plot_data_model_comparison


def make_figure(
    data_hist,
    background_hists,
    background_categories_labels,
    background_categories_colors,
):
    fig, ax_main, ax_comparison = plot_data_model_comparison(
        data_hist=data_hist,
        stacked_components=background_hists,
        stacked_labels=background_categories_labels,
        stacked_colors=background_categories_colors,
        xlabel=f"${key}\\,\\,[eV/c^2]$",
        ylabel="Hits in the LMN per $4.2\\times 10^{-1}\\,\\,eV/c^2$",
        comparison="pull",
        model_uncertainty=False,  # <--
    )

    add_luminosity(collaboration="plothist", ax=ax_main, is_data=False)

    return fig


if __name__ == "__main__":
    fig = make_figure(
        data_hist,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    )
    fig.savefig("model_examples_pull_no_model_unc.svg", bbox_inches="tight")
