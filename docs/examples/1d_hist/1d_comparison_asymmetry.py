"""
Asymmetry
=========

Compare two 1D histograms using the asymmetry comparison [(h1-h2)/(h1+h2)].
"""

from __future__ import annotations

from plothist import get_dummy_data

df = get_dummy_data()

name = "variable_1"

x1 = df[name][df["category"] == 2]
x2 = df[name][df["category"] == 3]

x_range = (min(*x1, *x2), max(*x1, *x2))

from plothist import make_hist

h1 = make_hist(x1, bins=50, range=x_range)
h2 = make_hist(x2, bins=50, range=x_range)

###
from plothist import plot_two_hist_comparison

fig, ax_main, ax_comparison = plot_two_hist_comparison(
    h1,
    h2,
    xlabel=name,
    ylabel="Entries",
    h1_label="$\mathbfit{h}_1$",
    h2_label="$\mathbfit{h}_2$",
    comparison="asymmetry",  # <--
)

fig.savefig("1d_comparison_asymmetry.svg", bbox_inches="tight")
