"""
1d side by side
===============

Plot multiple 1d histogram with categories side by side.

"""

###
import boost_histogram as bh
import numpy as np
import matplotlib.pyplot as plt
import plothist

rng = np.random.default_rng(8311311)

# Integer categories
categories = ["A", "B", "C"]
## Work also with integers
# categories = [-5, 10, 137]

# Axis with the 3 bins
axis = bh.axis.StrCategory(categories=categories)

# Generate data for 3 histograms
data = [
    rng.choice(categories, 20),
    rng.choice(categories, 30),
    rng.choice(categories, 40),
]

# Create and fill the histograms
histos = [bh.Histogram(axis, storage=bh.storage.Weight()) for _ in range(len(data))]
histos = [histo.fill(data[i]) for i, histo in enumerate(histos)]

# Convert the histograms to numpy arrays
histo_arrays = [histo.values() for histo in histos]

# Create an array for the x-coordinates of the bars
x = np.arange(len(axis))


# Get the correct shift for each bar
def calculate_shifts(width, n_bars):
    half_width = width / 2
    shift = np.linspace(-half_width, half_width, n_bars, endpoint=False)
    shift += width / (2 * n_bars)
    return shift


bin_width = 0.7
n_bars = len(histos)
shift = calculate_shifts(bin_width, n_bars)

fig, ax = plt.subplots()

# Plot the histograms side by side
for i, histo in enumerate(histo_arrays):
    bars = ax.bar(
        x + shift[i], histo, width=bin_width / n_bars, label=f"$\mathit{{h_{i}}}$"
    )

    # Optional: Add the number on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.1,
            int(height),
            ha="center",
            va="bottom",
        )

# Label the x-ticks with the categories
ax.set_xticks(x, axis)
ax.set_ylim(top=np.max([np.max(histo) for histo in histo_arrays]) + 2)
ax.minorticks_off()

ax.set_ylabel("Entries")
ax.set_xlabel("Categories")
ax.legend()

fig.savefig("1d_side_by_side.svg", bbox_inches="tight")
