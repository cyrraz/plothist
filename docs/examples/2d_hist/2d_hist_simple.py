"""
2d hist simple
==============

This example shows how to plot a 2d histogram with plothist.
"""

from plothist.get_dummy_data import get_dummy_data

df = get_dummy_data()

###
from plothist import make_2d_hist, plot_2d_hist
import matplotlib.pyplot as plt

name_x = "variable_0"
name_y = "variable_1"

h = make_2d_hist([df[name_x], df[name_y]])

fig, ax, ax_colorbar = plot_2d_hist(h, colorbar_kwargs={"label": "Entries"})

ax.set_xlabel(name_x)
ax.set_ylabel(name_y)

ax.set_xlim(-9, 9)
ax.set_ylim(-9, 9)

fig.savefig("2d_hist_simple.svg", bbox_inches="tight")
