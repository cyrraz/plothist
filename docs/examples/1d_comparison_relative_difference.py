"""
This example shows how to compare two 1D histograms using the relative difference.
"""

from plothist.generate_dummy_data import generate_dummy_data
df = generate_dummy_data()

from plothist import compare_two_hist

fig, ax_main, ax_comparison = compare_two_hist(
    h2,
    h3,
    xlabel=name,
    ylabel="Entries",
    h1_label="$\mathbf{H\,\,1}$",
    h2_label="$\mathbf{H\,\,2}$",
    comparison = "relative_difference", # <--
    save_as="1d_comparison_relative_difference.svg",
)