"""
2D histograms
=============

Plot multiple 2D histograms with the variable registry.
"""

from plothist_utils import get_dummy_data

df = get_dummy_data()

###
import os
from itertools import combinations

from plothist import (
    create_variable_registry,
    get_variable_from_registry,
    make_2d_hist,
    plot_2d_hist,
    update_variable_registry_ranges,
)

# No need to redo this step if the registry was already created before
variable_keys = ["variable_0", "variable_1", "variable_2"]
temporary_registry_path = "./_temporary_variable_registry.yaml"
create_variable_registry(variable_keys, path=temporary_registry_path)
update_variable_registry_ranges(df, variable_keys, path=temporary_registry_path)

# Get all the correlation plot between the variables
variable_keys_combinations = list(combinations(variable_keys, 2))

figs = []

for variable_keys_combination in variable_keys_combinations:
    variable0 = get_variable_from_registry(
        variable_keys_combination[0], path=temporary_registry_path
    )
    variable1 = get_variable_from_registry(
        variable_keys_combination[1], path=temporary_registry_path
    )

    h = make_2d_hist(
        [df[variable0["name"]], df[variable1["name"]]],
        bins=(variable0["bins"], variable1["bins"]),
        range=(variable0["range"], variable1["range"]),
    )

    fig, ax, ax_colorbar = plot_2d_hist(h, colorbar_kwargs={"label": "Entries"})

    ax.set_xlabel(variable0["name"])
    ax.set_ylabel(variable1["name"])

    ax.set_xlim(variable0["range"])
    ax.set_ylim(variable1["range"])

    figs.append(fig)

for i, fig in enumerate(figs):
    fig.savefig(f"2d_hist_correlations_{i}.svg", bbox_inches="tight")

os.remove(temporary_registry_path)
