"""
Mean histogram (profile)
========================

Plot a 1D mean histogram (profile).
"""

###
import boost_histogram as bh
import matplotlib.pyplot as plt

from plothist import plot_error_hist

# Regular axis with 3 bins from -1 to 1
axis = bh.axis.Regular(3, -1, 1)

# 6 data points, two in each bin
data = [-0.5, -0.5, 0.0, 0.0, 0.5, 0.5]
sample = [0, 100, 40, 60, 0, 20]
weights = [1, 1, 1, 1, 1, 1]

h = bh.Histogram(axis, storage=bh.storage.WeightedMean())
h.fill(data, weight=weights, sample=sample)

fig, ax = plt.subplots()

plot_error_hist(h, ax=ax)

ax.set_xlabel("Variable")
ax.set_ylabel("Mean")
ax.set_xlim(-1, 1)

fig.savefig("1d_profile.svg", bbox_inches="tight")
