"""
Stack histograms
================

Stack two 1D histograms with ``plot_hist()``.
"""

from plothist_utils import get_dummy_data

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
fig, ax = plt.subplots()

plot_hist(
    [h1, h2],
    label=["c1", "c2"],
    ax=ax,
    edgecolor="black",
    linewidth=0.5,
    histtype="stepfilled",
    stacked=True,
)

ax.set_xlabel(name)
ax.set_ylabel("Entries")
ax.set_xlim(x_range)
ax.legend()

fig.savefig("1d_elt1_stacked.svg", bbox_inches="tight")
