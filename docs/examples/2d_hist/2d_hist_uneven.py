"""
2D histogram, uneven binning
============================

Plot a 2D histogram with uneven binning.
"""

from plothist_utils import get_dummy_data

df = get_dummy_data()

###
from plothist import make_2d_hist, plot_2d_hist

name_x = "variable_0"
name_y = "variable_1"
# Bins [-10,0], [0,10] for variable 1,
# and bins [-10,-5], [-5,0], [0,5], [5,10] for variable 2
bins = [[-10, 0, 10], [-10, -5, 0, 5, 10]]

h = make_2d_hist([df[name_x], df[name_y]], bins=bins)

fig, ax, ax_colorbar = plot_2d_hist(h, colorbar_kwargs={"label": "Entries"})

ax.set_xlabel(name_x)
ax.set_ylabel(name_y)

fig.savefig("2d_hist_uneven.svg", bbox_inches="tight")
