"""
1d hist stacked
===============

This example shows how to stack two 1d histogram with plothist.
"""

from plothist.generate_dummy_data import generate_dummy_data
df = generate_dummy_data()

###
fig2, ax2 = plt.subplots()

plot_hist(
    [h1, h2],
    label=["c1", "c2"],
    ax=ax2,
    edgecolor="black",
    linewidth=0.5,
    histtype="stepfilled",
    stacked=True,
)

ax2.set_xlabel(name)
ax2.set_ylabel("Entries")
ax2.set_xlim(x_range)
ax2.legend()

fig2.savefig("1d_elt1_stacked.svg", bbox_inches="tight")