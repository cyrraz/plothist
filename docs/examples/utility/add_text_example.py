"""
Add text
========

Examples of use of ``add_text()``.
"""

###
from __future__ import annotations

import matplotlib.pyplot as plt

from plothist import add_text

fig, ax = plt.subplots()

positions = [
    ("right_in", "top_in"),
    ("left_in", "top_in"),
    ("left_in", "bottom_in"),
    ("right_in", "bottom_in"),
    ("right", "top_out"),
    ("left", "top_out"),
    ("right_out", "top_in"),
    ("right_out", "bottom_in"),
    ("right", "bottom_out"),
    ("left", "bottom_out"),
]

for x, y in positions:
    x_label = x.replace("_", "\_")
    y_label = y.replace("_", "\_")
    add_text(
        f"$\\mathtt{{add\\_text()}}$\n"
        f'$\\mathtt{{x = }}$"$\\mathtt{{{x_label}}}$"\n'
        f'$\\mathtt{{y = }}$"$\\mathtt{{{y_label}}}$"',
        x=x,
        y=y,
    )

fig.savefig("add_text_example.svg", bbox_inches="tight")
