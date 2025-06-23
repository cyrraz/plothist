"""
Function
========

Plot a 1D function with ``plot_function()``.
"""

###
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from scipy.stats import norm

from plothist import plot_function


def make_figure() -> Figure:
    # Define the gaussian function of mean=0.5 and std_dev=3
    def f(x):
        return 1000 * norm.pdf(x, loc=0.5, scale=3)

    fig, ax = plt.subplots()

    plot_function(f, range=[-10, 10], ax=ax)

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")

    return fig


if __name__ == "__main__":
    fig = make_figure()
    fig.savefig("fct_1d.svg", bbox_inches="tight")
