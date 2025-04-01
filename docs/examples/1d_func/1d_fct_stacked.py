"""
Stacked functions
=================

Plot stacked functions using ``plot_function()``.
"""

from __future__ import annotations

from scipy.stats import norm


# Define the gaussian function of mean=0.5 and std_dev=3
def f(x):
    return 1000 * norm.pdf(x, loc=0.5, scale=3)


###
from matplotlib import pyplot as plt

from plothist import plot_function


# Another function
def g(x):
    return 1000 * norm.pdf(x, loc=2, scale=3)


fig, ax = plt.subplots()

plot_function(
    [f, g],
    range=[-10, 10],
    ax=ax,
    labels=["f1", "f2"],
    stacked=True,
)

ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_ylim(0)
ax.legend()

fig.savefig("1d_fct_stacked.svg", bbox_inches="tight")
