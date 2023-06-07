import matplotlib.pyplot as plt
from itertools import combinations
from plothist.generate_dummy_data import generate_dummy_data
from plothist import (
    make_hist,
    make_2d_hist,
    plot_hist,
    plot_2d_hist,
    compare_two_hist,
    create_variable_registry,
    get_variable_from_registry,
    update_variable_registry_ranges,
)

# Generate dummy data
df = generate_dummy_data()

# I. How to plot a single variable
name = "variable_0"

fig, ax = plt.subplots()

h = make_hist(df[name])

plot_hist(h, ax=ax)

ax.set_xlabel(name)
ax.set_ylabel("Entries")


# II. How to plot a set of variable_keys using a variable registry
variable_keys = ["variable_0", "variable_1", "variable_2"]

# Create the yaml file containing all the plotting information
create_variable_registry(variable_keys)
# If no range specified for some variable_keys, update them with actual min and max value
update_variable_registry_ranges(df, variable_keys)

for variable_key in variable_keys:
    variable = get_variable_from_registry(variable_key)

    fig, ax = plt.subplots()
    h = make_hist(df[variable["name"]], bins=variable["bins"], range=variable["range"])
    plot_hist(h, ax=ax)
    ax.set_xlabel(variable["label"])

    ax.set_xlim(variable["range"])
    ax.set_ylabel("Entries")


# III. Compare one variable between two datasets
name = "variable_0"
category = "category"

x1 = df[name][df[category] == 1]
x2 = df[name][df[category] == 2]

x_range = [min([min(x) for x in [x1, x2]]), max([max(x) for x in [x1, x2]])]

h1 = make_hist(x1, bins=50, range=x_range, weights=1)
h2 = make_hist(x2, bins=50, range=x_range, weights=1)

compare_two_hist(
    h1, h2, xlabel=name, ylabel="Entries", x1_label="c1", x2_label="c2", save_as=None
)

# # IV. Compare a set of variable between two datasets using a registry

for variable_key in variable_keys:
    variable = get_variable_from_registry(variable_key)

    x1 = df[variable_key][df[category] == 1]
    x2 = df[variable_key][df[category] == 2]

    x_range = [min([min(x) for x in [x1, x2]]), max([max(x) for x in [x1, x2]])]

    h1 = make_hist(x1, bins=50, range=x_range, weights=1)
    h2 = make_hist(x2, bins=50, range=x_range, weights=1)

    compare_two_hist(
        h1,
        h2,
        xlabel=variable["label"],
        ylabel="Entries",
        x1_label="c1",
        x2_label="c2",
        save_as=None,
    )

# # V. How to plot a 2d histogram
# Basic 2D

name_x = "variable_0"
name_y = "variable_1"

fig, ax = plt.subplots(figsize=(4, 4))

h = make_2d_hist([df[name_x], df[name_y]])

plot_2d_hist(h, ax=ax, colorbar_kwargs={"label": "Entries"})

ax.set_xlabel(name_x)
ax.set_ylabel(name_y)

ax.set_xlim(-9, 9)
ax.set_ylim(-9, 9)


# Un-even binning

name_x = "variable_0"
name_y = "variable_1"
# Bins [-10,0], [0,10] for variable 1,
# and bins [-10,-5], [-5,0], [0,5], [5,10] for variable 2
bins = [[-10, 0, 10], [-10, -5, 0, 5, 10]]

fig, ax = plt.subplots(figsize=(4, 4))

h = make_2d_hist([df[name_x], df[name_y]], bins=bins)

plot_2d_hist(h, ax=ax, colorbar_kwargs={"label": "Entries"})

ax.set_xlabel(name_x)
ax.set_ylabel(name_y)


# With variable manager

# Create the yaml file containing all the plotting information
# Already created in II., no need to redo it here
# variable_keys = ["variable_0", "variable_1", "variable_2"]
# create_variable_registry(variable_keys)
# update_variable_registry_ranges(df, variable_keys)

# Get all the correlation plot between the variables
variable_keys_combinations = list(combinations(variable_keys, 2))
for variable_keys_combination in variable_keys_combinations:
    variable0 = get_variable_from_registry(variable_keys_combination[0])
    variable1 = get_variable_from_registry(variable_keys_combination[1])

    fig, ax = plt.subplots(figsize=(4, 4))

    h = make_2d_hist(
        [df[variable0["name"]], df[variable1["name"]]],
        bins=(variable0["bins"], variable1["bins"]),
        range=(variable0["range"], variable1["range"]),
    )

    plot_2d_hist(h, ax=ax, colorbar_kwargs={"label": "Entries"})

    ax.set_xlabel(variable0["name"])
    ax.set_ylabel(variable1["name"])

    ax.set_xlim(variable0["range"])
    ax.set_ylim(variable1["range"])


plt.show()
