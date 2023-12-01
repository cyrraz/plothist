"""
2d with projections
===================

This example shows how to plot a 2d histogram with the projections of the 1d distributions.
"""

from plothist.generate_dummy_data import generate_dummy_data

df = generate_dummy_data()

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
