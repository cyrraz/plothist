"""
1d function
===========

Plot a function with ``plot_function``.
"""
###
from plothist import plot_function
from scipy.stats import norm
from matplotlib import pyplot as plt


# Define the gaussian function of mean=0.5 and std_dev=3
def f(x):
    return 1000 * norm.pdf(x, loc=0.5, scale=3)


fig, ax = plt.subplots()

plot_function(f, range=[-10, 10], ax=ax)

ax.set_xlabel("x")
ax.set_ylabel("f(x)")

fig.savefig("1d_fct.svg", bbox_inches="tight")
