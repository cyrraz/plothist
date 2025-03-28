"""
Stack histograms
================

Stack two 1D histograms with ``plot_hist()``.
"""

from plothist import get_dummy_data

df = get_dummy_data()

import matplotlib.pyplot as plt

from plothist import make_hist, plot_hist

name = "variable_1"
category = "category"

x1 = df[name][df[category] == 1]
x2 = df[name][df[category] == 2]

x_range = (min(*x1, *x2), max(*x1, *x2))

h1 = make_hist(x1, bins=50, range=x_range)
h2 = make_hist(x2, bins=50, range=x_range)

###
fig2, ax2 = plt.subplots()

plot_hist(
    [h1, h2],
    label=["c1", "c2"],
    ax=ax2,
    edgecolor="black",
    linewidth=0.5,
    histtype="fill",
    stack=True,
)

ax2.set_xlabel(name)
ax2.set_ylabel("Entries")
ax2.set_xlim(x_range)
ax2.legend()

fig2.savefig("1d_elt1_stacked.svg", bbox_inches="tight")
