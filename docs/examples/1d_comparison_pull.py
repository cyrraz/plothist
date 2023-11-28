"""
This example shows how to compare two 1D histograms using the pull method.
"""

from plothist.generate_dummy_data import generate_dummy_data
df = generate_dummy_data()

from plothist import compare_two_hist

# Default comparison is ratio
fig, ax_main, ax_comparison = compare_two_hist(
    h2,
    h3,
    xlabel=name,
    ylabel="Entries",
    h1_label="$c_2$",
    h2_label="$c_3$",
    comparison="pull", # <---
    save_as="1d_comparison_ratio.svg",
)