"""
1d hist simple
==============

This example shows how to plot a 1d histogram with plothist.
"""

from plothist.generate_dummy_data import generate_dummy_data
df = generate_dummy_data()

###
from plothist import make_hist, plot_hist, set_style
import matplotlib.pyplot as plt

name = "variable_0"

fig, ax = plt.subplots()

h = make_hist(df[name])

plot_hist(h, ax=ax)

ax.set_xlabel(name)
ax.set_ylabel("Entries")

fig.savefig("1d_hist_simple.svg", bbox_inches='tight')