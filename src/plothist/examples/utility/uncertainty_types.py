"""
Representation of different uncertainty types.
==============================================

This example demonstrates how to use the `plot_error_hist` function with different uncertainty types
"""

import boost_histogram as bh
import matplotlib.pyplot as plt
import numpy as np

from plothist import add_text, plot_error_hist


def shifted_array(values, offset: int, size: int = 15) -> np.ndarray:
    """
    Create an array of a given size with NaNs and fill it with values at specified offsets.
    The values are inserted at every offset starting from the given offset.
    """

    arr = np.full(size, np.nan)
    indices = range(offset, size, len(values))

    for i, idx in enumerate(indices):
        if i >= len(values):
            break
        arr[idx] = values[i]

    return arr


def make_grouped_edges(
    n_groups, group_size=4, inner_spacing=0.1, inter_spacing=0.2
) -> np.ndarray:
    """
    Create a set of edges for a histogram with grouped categories.
    """

    edges = [
        group_start + i * inner_spacing
        for group in range(n_groups)
        for i in range(group_size)
        for group_start in [
            group * (group_size * inner_spacing + inter_spacing - inner_spacing)
        ]
    ]
    return np.array(edges)


# Create a category axis with explicit locations
edges = make_grouped_edges(4)
axis = bh.axis.Variable(edges)

hists = []
entries = [0, 0.5, 3, 500]

for k in range(3):
    hist = bh.Histogram(axis, storage=bh.storage.Weight())
    values = shifted_array(entries, k)
    hist[:] = np.c_[values, values]
    hists.append(hist)


fig, (ax_top, ax_bot) = plt.subplots(
    2, 1, gridspec_kw={"height_ratios": [1, 3], "hspace": 0.05}
)

for ax in (ax_top, ax_bot):
    plot_error_hist(
        hists[0], ax=ax, label="symmetrical", uncertainty_type="symmetrical"
    )
    plot_error_hist(
        hists[1], ax=ax, label="asymmetrical", uncertainty_type="asymmetrical"
    )
    plot_error_hist(
        hists[2],
        ax=ax,
        label="asymmetrical_double_sided",
        uncertainty_type="asymmetrical_double_sided",
    )

add_text("plot_error_hist() with different uncertainty type", ax=ax_top, x="right")

# Set axis limits
ax_top.set_ylim(465, 530)
ax_bot.set_ylim(-0.5, 6.9)
ax_bot.set_xlim(xmin=-0.05)

# Format bottom ticks and labels
ax_bot.set_xticks(edges[1::4] + 0.05)
ax_bot.set_xlabel("Entry category")
ax_bot.set_xticklabels(entries)
ax_bot.set_ylabel("Entries")
ax_bot.yaxis.label.set_horizontalalignment("left")
ax_bot.spines.top.set_visible(False)
ax_bot.xaxis.set_minor_locator(plt.NullLocator())  # Hide x-axis minor ticks

# Format top ticks and labels
ax_top.xaxis.tick_top()
ax_top.spines.bottom.set_visible(False)
ax_top.set_xticklabels([])
ax_top.set_xticks([])

# Draw break marks
d = 0.5  # proportion of vertical to horizontal extent of the slanted line
kwargs = {
    "marker": [(-1, -d), (1, d)],
    "markersize": 12,
    "linestyle": "none",
    "color": "k",
    "mec": "k",
    "mew": 1,
    "clip_on": False,
}
ax_top.plot([0, 1], [0, 0], transform=ax_top.transAxes, **kwargs)
ax_bot.plot([0, 1], [1, 1], transform=ax_bot.transAxes, **kwargs)

ax_top.legend(loc="upper left")

fig.savefig("uncertainty_types.svg", bbox_inches="tight")
