"""
Pull comparison
===============

This example shows how to compare two 1D histograms using the pull method.
"""

from plothist.get_dummy_data import get_dummy_data

df = get_dummy_data()

name = "variable_1"

x2 = df[name][df["category"] == 2]
x3 = df[name][df["category"] == 3]

x_range = (min(min(x2), min(x3)), max(max(x2), max(x3)))

from plothist import make_hist

h2 = make_hist(x2, bins=50, range=x_range)
h3 = make_hist(x3, bins=50, range=x_range)

###
from plothist import plot_two_hist_comparison

# Default comparison is ratio
fig, ax_main, ax_comparison = plot_two_hist_comparison(
    h2,
    h3,
    xlabel=name,
    ylabel="Entries",
    h1_label="$c_2$",
    h2_label="$c_3$",
    comparison="pull",  # <---
)

fig.savefig("1d_comparison_pull.svg", bbox_inches="tight")
