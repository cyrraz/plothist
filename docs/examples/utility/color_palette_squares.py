"""
Color palette squares
=====================

Create a plot of a color palette with squares representing the color gradient of the palette.
"""


import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.colors as mcolors
from plothist import get_color_palette


def create_palette_plot(colors, fig_name, add_text=False, add_black_border=False):
    ncolors = len(colors)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(ncolors, 1))

    # Plot the colored squares with small spacing
    square_size = 1
    spacing = 0.1
    x = 0

    for color in colors:
        rect = patches.Rectangle((x, 0), square_size, square_size, color=color)
        ax.add_patch(rect)
        x += square_size + spacing

        if add_text:
            # Add text displaying the color value
            ax.text(
                x - (square_size + spacing) / 1.81,
                -0.18,
                mcolors.rgb2hex(color).upper(),
                ha="center",
                fontsize=10,
            )

    # Set the x-axis limits and show the ticks
    ax.set_xlim(-0.5, x - spacing)
    ax.set_xticks(np.arange(0, x, square_size + spacing))
    ax.set_xticklabels(np.arange(1, ncolors + 1), fontsize=8)
    ax.set_xticklabels([])  # Remove the x-tick labels

    # Set the y-axis ticks and labels
    ax.set_yticks([])
    ax.set_yticklabels([])

    # Remove the borders around the plot
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Remove the x-label and y-label
    ax.set_xlabel("")
    ax.set_ylabel("")

    if add_black_border:
        # Add a black border rectangle
        border_rect = patches.Rectangle(
            (0, 0),
            x - spacing,
            square_size,
            edgecolor="black",
            facecolor="none",
            linewidth=1,
        )
        ax.add_patch(border_rect)

    # Adjust the padding and remove extra whitespace
    plt.margins(0)
    plt.gca().set_axis_off()
    plt.subplots_adjust(left=0.05, right=0.95)

    plt.savefig(fig_name, bbox_inches="tight")


ncolors = 7

if ncolors > 7:
    ncolors_ggplot = 7
else:
    ncolors_ggplot = ncolors
colors = get_color_palette("ggplot", ncolors_ggplot)
create_palette_plot(colors, fig_name="usage_style_cycle.svg", add_text=True)

colors = get_color_palette("cubehelix", ncolors)
create_palette_plot(colors, fig_name="usage_cubehelix.svg")

cmap_list = ["viridis", "coolwarm", "YlGnBu_r"]
for cmap_name in cmap_list:
    colors = get_color_palette(cmap_name, ncolors)
    create_palette_plot(colors, fig_name=f"usage_{cmap_name}_palette.svg")
