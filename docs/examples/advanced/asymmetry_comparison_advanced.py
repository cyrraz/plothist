"""
Advanced example using asymmetry comparison
===========================================

Plot the asymmetry between 2 histograms and 2 functions.
"""


# Get dummy data
from plothist.get_dummy_data import get_dummy_data

df = get_dummy_data()

###
from scipy.stats import norm
import numpy as np
from plothist import (
    create_comparison_figure,
    make_hist,
    plot_error_hist,
    plot_function,
    plot_comparison,
    add_luminosity,
    add_text,
)


# Define some random functions that will be used as Data fit functions
def f1(x):
    return 4000 * norm.pdf(x, loc=-0.5, scale=1.6)


def f2(x):
    return 4000 * norm.pdf(x, loc=0.5, scale=1.6)


name = "variable_1"
category = "category"

x1 = df[name][df[category] == 5]

x_range = [-9, 9]

# Create the histograms used as data
h1 = make_hist(x1 - 2.5, bins=50, range=x_range)
h2 = make_hist(x1 - 1.5, bins=50, range=x_range)

# Create the figure
fig, (ax_main, ax_comparison) = create_comparison_figure(
    gridspec_kw={"height_ratios": [2, 1]}
)

# Define the marker style
marker_1 = {
    "color": "tab:red",
    "markeredgecolor": "tab:red",
    "ls": "None",
    "fmt": "o",
    "markersize": 5,
    "label": "$Data_1$",
}

marker_2 = {
    "color": "tab:blue",
    "markerfacecolor": "white",
    "markeredgecolor": "tab:blue",
    "ls": "None",
    "fmt": "o",
    "markersize": 5,
    "label": "$Data_2$",
}

# Plot the data
plot_error_hist(
    h1,
    ax_main,
    **marker_1,
)

plot_error_hist(
    h2,
    ax_main,
    **marker_2,
)

# Plot the functions
plot_function(f1, x_range, ax_main, color=marker_1["color"], label="Data$_1$ fit")
plot_function(
    f2, x_range, ax_main, color=marker_2["color"], linestyle="--", label="Data$_2$ fit"
)

# Plot the asymmetry comparison between the 2 histograms
plot_comparison(
    h1,
    h2,
    ax=ax_comparison,
    h1_label="$Data_1$",
    h2_label="$Data_2$",
    comparison="asymmetry",
    comparison_ylim=(-1, 1)
)

# Define the asymmetry of the 2 functions
asymmetry = lambda x: (f1(x) - f2(x)) / (f1(x) + f2(x))

# Plot the asymmetry of the 2 functions
plot_function(asymmetry, x_range, ax_comparison, color="black")

ax_main.legend()

fig.align_ylabels()

ax_main.set_xlim(x_range)
ax_main.set_ylim(ymin=0)
ax_main.set_ylabel("Entries")
ax_main.legend()

ax_comparison.set_xlim(x_range)
ax_comparison.set_xlabel(name)

add_text("Data and fit asymmetry comparison", ax=ax_comparison, x="right")

add_luminosity(collaboration="LMN 3", ax=ax_main, lumi="(1 + 0.3)", preliminary=True, x="left")

fig.savefig("asymmetry_comparison_advanced.svg", bbox_inches="tight")
