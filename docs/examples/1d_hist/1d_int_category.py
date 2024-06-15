"""
Integer categories
==================

Plot a 1D histogram with integer categories.
"""

###
import boost_histogram as bh
from plothist import plot_hist
import matplotlib.pyplot as plt

# 3 integer categories
int_categories = [-10, 5, 72]

# Integer category axis with 3 bins
axis = bh.axis.IntCategory(categories=int_categories)

# 6 data points,
data = [-10, -10, 5, 72, 72, 72]

# Create and fill the histogram
h = bh.Histogram(axis, storage=bh.storage.Weight())
h.fill(data)

# Plot the histogram
fig, ax = plt.subplots()

plot_hist(h, ax=ax)

# Set the x-ticks to the middle of the bins and label them
ax.set_xticks([i + 0.5 for i in range(len(int_categories))])
ax.set_xticklabels(int_categories)
ax.minorticks_off()

ax.set_xlabel("Integer Category")
ax.set_ylabel("Entries")
ax.set_xlim(0, len(int_categories))

fig.savefig("1d_int_category.svg", bbox_inches="tight")
