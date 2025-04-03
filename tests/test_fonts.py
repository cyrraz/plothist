from __future__ import annotations

from pytest import fail


def test_fonts():
    """
    Test fonts.
    """
    import matplotlib.font_manager as fm

    import plothist  # NOQA: F401

    installation_failed = False
    for font_type in ["Math", "Sans", "Roman"]:
        try:
            fm.findfont(f"Latin Modern {font_type}", fallback_to_default=False)
        except ValueError:
            print(f"The font Latin Modern {font_type} was not found.")
            installation_failed = True

    if installation_failed:
        fail("At least one of the Latin Modern fonts was not installed correctly.")
