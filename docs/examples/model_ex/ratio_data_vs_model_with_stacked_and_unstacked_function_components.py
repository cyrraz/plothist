"""
Data vs functional model
========================

Compare data and model with stacked and unstacked functional components.
"""

from plothist import get_dummy_data

df = get_dummy_data()

from plothist import make_hist, get_color_palette

# Define the histograms

key = "variable_1"
range = [-9, 12]
category = "category"

# Define masks
data_mask = df[category] == 8

# Make histograms
data_hist = make_hist(df[key][data_mask], bins=50, range=range, weights=1)

# Define some random functions that will be used as model components with functions
from scipy.stats import norm


def f_signal(x):
    return 1000 * norm.pdf(x, loc=0.5, scale=3)


def f_background1(x):
    return 1000 * norm.pdf(x, loc=-1.5, scale=4)


def f_background2(x):
    return 3000 * norm.pdf(x, loc=-1.8, scale=1.8)


###
from plothist import plot_data_model_comparison

fig, ax_main, ax_comparison = plot_data_model_comparison(
    data_hist=data_hist,
    stacked_components=[f_background1, f_background2],
    stacked_labels=["c0", "c1"],
    unstacked_components=[f_signal],
    unstacked_labels=["Signal"],
    unstacked_colors=["#8EBA42"],
    xlabel=key,
    ylabel="Entries",
    model_sum_kwargs={"show": True, "label": "Model", "color": "navy"},
    comparison="pull",
)

fig.savefig(
    "ratio_data_vs_model_with_stacked_and_unstacked_function_components.svg",
    bbox_inches="tight",
)
