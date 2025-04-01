"""
2D histograms
=============

Plot multiple 2D histograms with the variable registry.
"""

from plothist import get_dummy_data

df = get_dummy_data()

###
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
create_variable_registry(variable_keys)
update_variable_registry_ranges(df, variable_keys)

# Get all the correlation plot between the variables
variable_keys_combinations = list(combinations(variable_keys, 2))

for k_combination, variable_keys_combination in enumerate(variable_keys_combinations):
    variable0 = get_variable_from_registry(variable_keys_combination[0])
    variable1 = get_variable_from_registry(variable_keys_combination[1])

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

    fig.savefig(f"2d_hist_correlations_{k_combination}.svg", bbox_inches="tight")
