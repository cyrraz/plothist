"""
2D histogram with projections
==============================

Plot a 2D histogram with the two 1D projections.
"""

from plothist import get_dummy_data

df = get_dummy_data()

###
from plothist import make_2d_hist, plot_2d_hist_with_projections

name_x = "variable_0"
name_y = "variable_1"

h = make_2d_hist([df[name_x], df[name_y]], bins=[50, 50])

(
    fig,
    ax_2d,
    ax_x_projection,
    ax_y_projection,
    ax_colorbar,
) = plot_2d_hist_with_projections(
    h,
    xlabel="variable_0",
    ylabel="variable_1",
    ylabel_x_projection="Entries",
    xlabel_y_projection="Entries",
    offset_x_labels=False,
    colorbar_kwargs={"label": "Entries"},
)

fig.savefig("2d_hist_with_projections.svg", bbox_inches="tight")
