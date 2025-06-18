from __future__ import annotations

import matplotlib.font_manager as fm
from pytest import fail

import plothist  # NOQA: F401


def test_fonts() -> None:
    """
    Test fonts.
    """

    installation_failed = False
    for font_type in ["Math", "Sans", "Roman"]:
        try:
            fm.findfont(f"Latin Modern {font_type}", fallback_to_default=False)
        except ValueError:
            print(f"The font Latin Modern {font_type} was not found.")
            installation_failed = True

    if installation_failed:
        fail("At least one of the Latin Modern fonts was not installed correctly.")
