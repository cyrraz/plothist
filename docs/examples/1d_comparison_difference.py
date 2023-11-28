"""
This example shows how to compare two 1D histograms using the difference method.
"""

from plothist.generate_dummy_data import generate_dummy_data
df = generate_dummy_data()

from plothist import compare_two_hist, add_text

fig, ax_main, ax_comparison = compare_two_hist(
    h2,
    h3,
    xlabel=name,
    ylabel="Entries",
    h1_label="$\mathcal{C}_{2}$",
    h2_label="$\mathcal{C}_{3}$",
    comparison = "difference", # <--
)

add_text("Comparison of two hist with difference plot", ax=ax_main)
add_text("Difference ax", x="right", ax=ax_comparison)

fig.savefig("1d_comparison_difference.svg", bbox_inches='tight')