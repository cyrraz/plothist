import matplotlib.pyplot as plt
from plothist.generate_dummy_data import generate_dummy_data
from plothist import (
    make_hist,
    plot_hist,
    plot_error_hist,
    plot_hist_difference,
    cubehelix_palette,
)


# Generate dummy data
df = generate_dummy_data()


# I How to plot multiple data categories
key = "variable_1"
range = [-10, 10]
category = "category"

# Define masks

unstacked_mask = df[category] == 7
error_mask = df[category] == 8

stacked_categories = [0, 1, 2, 3, 4, 5, 6]
stacked_categories_labels = [f"c{i}" for i in stacked_categories]
stacked_categories_colors = cubehelix_palette(
    ncolors=len(stacked_categories),
    start=1.5,
    rotation=1.5,
    darkest=0.3,
    lightest=0.8,
    reverse=True,
)
stacked_masks = [df[category] == p for p in stacked_categories]

# Make histograms

error_hist = make_hist(df[key][error_mask], bins=10, range=range, weights=1)
stacked_hist = [
    make_hist(df[key][mask], bins=10, range=range, weights=1) for mask in stacked_masks
]
unstacked_hist = make_hist(df[key][unstacked_mask], bins=10, range=range, weights=1)

# Optional: normalisation to error_data

stacked_hist_scaling_factor = error_hist.sum().value / sum(stacked_hist).sum().value
stacked_hist = [stacked_hist_scaling_factor * h for h in stacked_hist]

unstacked_hist_scaling_factor = error_hist.sum().value / unstacked_hist.sum().value
unstacked_hist *= unstacked_hist_scaling_factor

# Plot the histograms

fig, ax = plt.subplots()

plot_hist(
    stacked_hist,
    ax=ax,
    stacked=True,
    color=stacked_categories_colors,
    label=stacked_categories_labels,
    edgecolor="black",
    histtype="stepfilled",
    linewidth=0.5,
)
plot_hist(
    unstacked_hist, ax=ax, stacked=False, color="red", label="Signal", histtype="step"
)
plot_error_hist(error_hist, ax=ax, color="black", label="Data")

ax.legend(ncol=1, framealpha=0.1, fontsize=10)

ax.set_xlabel(key)
ax.set_ylabel("Entries")

# Optional: save the figure
# fig.savefig('test.pdf', bbox_inches='tight')

# II Plot histogram difference
fig, ax = plt.subplots()
plot_hist_difference(error_hist, sum(stacked_hist), ax)
ax.set_xlabel(key)
ax.set_ylabel("Difference")

plt.show()
