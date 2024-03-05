"""
Matplotlib vs plothist style
============================

This example shows the difference between matplotlib and plothist default style.
"""

import matplotlib.pyplot as plt

from plothist import get_dummy_data

df = get_dummy_data()

for style in ["matplotlib", "plothist"]:
    if style == "matplotlib":
        plt.style.use("default")
    else:
        # No need to set the style if we use plothist, just importing it is enough
        # Here we set the style because the matplotlib style was set before
        from plothist import set_style

        set_style("default")

    # Create a figure with subplots
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(6, 5.4), sharex=True, gridspec_kw={"height_ratios": [4, 1]}
    )

    # Plot histograms in the first subplot (ax1)
    hist_0, bins, _ = ax1.hist(
        df["variable_0"], bins=20, histtype="step", linewidth=1.2, label="h1"
    )
    h1 = ax1.hist(
        df["variable_1"], bins=bins, histtype="step", linewidth=1.2, label="h2"
    )
    ax1.set_ylabel("Entries")
    ax1.legend()

    # Calculate the ratio of histogram values and plot in the second subplot (ax2)
    ratio = hist_0 / h1[0]  # Divide bin values of variable_0 by variable_1
    bin_centers = 0.5 * (bins[:-1] + bins[1:])  # Calculate bin centers

    # Create fake error bars for the ratio
    ax2.plot(bin_centers, ratio, marker="|", linestyle="", markersize=15, color="black")
    ax2.plot(bin_centers, ratio, marker="o", linestyle="", markersize=4, color="black")

    ax2.axhline(y=1, color="black", linestyle="--", linewidth=0.8)
    ax2.set_xlabel("Variable")
    ax2.set_ylabel("Ratio")

    ax1.set_xlim(-10, 10)
    ax2.set_xlim(-10, 9)
    ax2.set_ylim(0, 2)

    fig.subplots_adjust(hspace=0.15)

    fig.savefig(f"{style}_example.svg", bbox_inches="tight")
