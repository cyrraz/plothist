"""
Side-by-side categories, with numbers on top
============================================

Plot multiple 1D histograms with categories side by side, and add the number of entries on top of each bar.
"""

###
import boost_histogram as bh
import matplotlib.pyplot as plt
import numpy as np

from plothist import plot_hist

rng = np.random.default_rng(83113111)

# Integer categories
categories = [-137, 12, 1234]
axis = bh.axis.IntCategory(categories=categories)

# Generate data for 3 histograms
data = [
    rng.choice(categories, 50),
    rng.choice(categories, 30),
    rng.choice(categories, 35),
    rng.choice(categories, 30),
]

# Create and fill the histograms
histos = [bh.Histogram(axis, storage=bh.storage.Weight()) for _ in range(len(data))]
histos = [histo.fill(data[i]) for i, histo in enumerate(histos)]

labels = [f"$h_{{{i}}}$" for i in range(len(histos))]
colors = ["#348ABD", "#E24A33", "#988ED5", "#FBC15E"]

# Plot the histogram
fig, ax = plt.subplots()

# Use a specificity of matplotlib: when a list of histograms is given, it will plot them side by side unless stacked=True or histtype is a "step" type.
plot_hist(histos, ax=ax, label=labels, color=colors)


# Add the number of entries on top of each bar
# Get the correct shift in x-axis for each bar
def calculate_shifts(width, n_bars):
    half_width = width / 2
    shift = np.linspace(-half_width, half_width, n_bars, endpoint=False)
    shift += width / (2 * n_bars)
    return shift


bin_width = 0.8
shift = calculate_shifts(bin_width, len(histos))

# Loop over the histograms, add on top of each bar the number of entries
for i, histo in enumerate(histos):
    for j, value in enumerate(histo.values()):
        ax.text(
            j + 0.5 + shift[i],
            value,
            int(
                value
            ),  # If weighted, f"{height:.1f}" can be used as a better representation of the bin content
            color="black",
            ha="center",
            va="bottom",
        )

# Set the x-ticks to the middle of the bins and label them
ax.set_xlim(0, len(categories))
ax.set_xticks([i + 0.5 for i in range(len(categories))])
ax.set_xticklabels(categories)
ax.minorticks_off()
# Get nice looking y-axis ticks
ax.set_ylim(top=int(np.max([np.max(histo.values()) for histo in histos]) * 1.5))

ax.set_xlabel("Category")
ax.set_ylabel("Entries")
ax.legend()

fig.savefig("1d_side_by_side_with_numbers.svg", bbox_inches="tight")
