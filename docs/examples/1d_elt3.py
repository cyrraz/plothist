"""
1d with scipy example
=====================

This example shows how to mix plothist with matplotlib or scipy.
"""

from plothist.generate_dummy_data import generate_dummy_data
df = generate_dummy_data()

from plothist import make_hist, plot_hist
import matplotlib.pyplot as plt

name = "variable_1"
category = "category"

x1 = df[name][df[category] == 1]
x2 = df[name][df[category] == 2]

x_range = (min(min(x1), min(x2)), max(max(x1), max(x2)))

h1 = make_hist(x1, bins=50, range=x_range)
h2 = make_hist(x2, bins=50, range=x_range)

fig, ax = plt.subplots()

plot_hist(h1, ax=ax, histtype="step", linewidth=1.2, label="c1")
plot_hist(h2, ax=ax, histtype="step", linewidth=1.2, label="c2")

ax.set_xlabel(name)
ax.set_ylabel("Entries")
ax.set_xlim(x_range)
ax.legend()

from plothist import plot_error_hist

x3 = df[name][df[category] == 3]

h3 = make_hist(x3, bins=50, range=x_range)

plot_error_hist(h3, ax=ax, color="black", label="c3")

# Update the legend
ax.legend()

# fig.savefig("1d_elt2.svg", bbox_inches='tight')

import numpy as np
from scipy.stats import norm

x = np.linspace(x_range[0], x_range[1], 200)

# Define the gaussian function of mean=8 and std_dev=1
y = norm.pdf(x, 8, 1)

# Normalize the function
y *= 900 / max(y)

ax.plot(x, y, color='green', label='Gaussian')

# Update the legend
ax.legend()

fig.savefig("1d_elt3.svg", bbox_inches='tight')