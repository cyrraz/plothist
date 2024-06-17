"""
Histogram with uncertainties
============================

Plot a 1D histogram with error bars using ``plot_error_hist()``.
"""

from plothist import get_dummy_data

df = get_dummy_data()

###
from plothist import make_hist, plot_error_hist
import matplotlib.pyplot as plt

name = "variable_1"
category = "category"

x1 = df[name][df[category] == 3]

h1 = make_hist(x1)

fig, ax = plt.subplots()

plot_error_hist(h1, ax=ax, color="black", label="$h1_{err}$")

ax.set_xlabel(name)
ax.set_ylabel("Entries")
ax.set_ylim(ymin=0)
ax.legend()

fig.savefig("1d_elt2.svg", bbox_inches="tight")
