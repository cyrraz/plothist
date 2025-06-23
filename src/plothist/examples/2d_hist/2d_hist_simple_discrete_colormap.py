"""
2D histogram, discrete colormap
===============================

Plot a 2D histogram with ``plot_2d_hist()`` with a discrete colormap.
"""

from plothist_utils import get_dummy_data

df = get_dummy_data()

from plothist import make_2d_hist, plot_2d_hist

name_x = "variable_0"
name_y = "variable_1"

# We only take a subset of the data
nentries = 1000

h = make_2d_hist([df[name_x][:nentries], df[name_y][:nentries]], bins=[50, 50])

###
from matplotlib.colors import ListedColormap

from plothist import get_color_palette

# 0 entries will be white, the rest will have one color from the plasma colormap per entry value
cmap = ListedColormap(
    ["white", *list(get_color_palette("plasma", int(h.values().max()) * 2 - 1))]
)

fig, ax, ax_colorbar = plot_2d_hist(
    h, colorbar_kwargs={"label": "Entries"}, pcolormesh_kwargs={"cmap": cmap}
)

ax.set_xlabel(name_x)
ax.set_ylabel(name_y)

ax.set_xlim(-4.5, 4.5)
ax.set_ylim(-4.5, 4.5)

fig.savefig("2d_hist_simple_discrete_colormap.svg", bbox_inches="tight")
