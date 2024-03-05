"""
1d Simple hist
==============

Plot a 1d histogram with with ``plot_hist``.
"""

from plothist import get_dummy_data

df = get_dummy_data()

###
from plothist import make_hist, plot_hist
import matplotlib.pyplot as plt

name = "variable_0"

fig, ax = plt.subplots()

h = make_hist(df[name])

plot_hist(h, ax=ax)

ax.set_xlabel(name)
ax.set_ylabel("Entriess")

fig.savefig("1d_hist_simple.svg", bbox_inches="tight")
