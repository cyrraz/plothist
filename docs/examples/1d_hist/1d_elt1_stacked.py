"""
1d Stacked hists
================

Stack two 1d histograms with ``plot_hist`` function.
"""

from plothist import get_dummy_data

df = get_dummy_data()

from plothist import make_hist, plot_hist
import matplotlib.pyplot as plt

name = "variable_1"
category = "category"

x1 = df[name][df[category] == 1]
x2 = df[name][df[category] == 2]

x_range = (min(min(x1), min(x2)), max(max(x1), max(x2)))

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
    histtype="stepfilled",
    stacked=True,
)

ax2.set_xlabel(name)
ax2.set_ylabel("Entries")
ax2.set_xlim(x_range)
ax2.legend()

fig2.savefig("1d_elt1_stacked.svg", bbox_inches="tight")
