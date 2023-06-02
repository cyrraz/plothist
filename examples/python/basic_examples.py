import numpy as np
import matplotlib.pyplot as plt
import boost_histogram as bh

from plothist.plotters import make_hist
from plothist.plotters import plot_hist
from plothist.plotters import compare_two_hist
from plothist.plotters import Variable
from plothist.plotters import create_variable_registry
from plothist.plotters import get_variable_from_registry
from plothist.plotters import update_variable_registry_ranges
from plothist.generate_dummy_data import generate_dummy_data

# Generate dummy data
df = generate_dummy_data()

# I. How to plot a single variable
key = "variable_0"

fig, ax = plt.subplots()

h = make_hist(df[key])

plot_hist(h, ax=ax)

ax.set_xlabel(key)
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
key = "variable_0"
category = "category"

x1 = df[key][df[category] == 1]
x2 = df[key][df[category] == 2]

x_range = [min([min(x) for x in [x1, x2]]), max([max(x) for x in [x1, x2]])]

h1 = make_hist(x1, bins=50, range=x_range, weights=1)
h2 = make_hist(x2, bins=50, range=x_range, weights=1)

compare_two_hist(
    h1, h2, xlabel=key, ylabel="Entries", x1_label="c1", x2_label="c2", save_as=None
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

plt.show()
