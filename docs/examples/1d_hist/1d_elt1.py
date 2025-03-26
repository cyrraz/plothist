"""
Multiple histograms
===================

Plot multiple histograms on the same plot using ``plot_hist()``.
"""

from plothist import get_dummy_data

df = get_dummy_data()

###
import matplotlib.pyplot as plt

from plothist import make_hist, plot_hist

name = "variable_1"
category = "category"

x1 = df[name][df[category] == 1]
x2 = df[name][df[category] == 2]

x_range = (min(min(x1), min(x2)), max(max(x1), max(x2)))

h1 = make_hist(x1, bins=50, range=x_range)
h2 = make_hist(x2, bins=50, range=x_range)

fig, ax = plt.subplots()

plot_hist(h1, ax=ax, histtype="step", linewidth=1.2, label="c1")
plot_hist(h2, ax=ax, histtype="step", linewidth=1.2, label="c2")

ax.set_xlabel(name)
ax.set_ylabel("Entries")
ax.set_xlim(x_range)
ax.legend()

fig.savefig("1d_elt1.svg", bbox_inches="tight")
