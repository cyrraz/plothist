"""
Histogram
=========

Plot a 1D histogram with ``plot_hist()``.
"""

from plothist_utils import get_dummy_data

df = get_dummy_data()

###
import matplotlib.pyplot as plt

from plothist import make_hist, plot_hist

name = "variable_0"

fig, ax = plt.subplots()

h = make_hist(df[name])

plot_hist(h, ax=ax)

ax.set_xlabel(name)
ax.set_ylabel("Entries")

fig.savefig("1d_hist_simple.svg", bbox_inches="tight")
