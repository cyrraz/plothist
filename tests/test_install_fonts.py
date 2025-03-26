from pytest import fail
from plothist.scripts import install_latin_modern_fonts


def test_install_latin_modern_fonts():
    """
    Test install_latin_modern_fonts.
    """

    install_latin_modern_fonts()

    # Reload the matplotlib cache
    from matplotlib.font_manager import _load_fontmanager

    new_fontmanager = _load_fontmanager(try_read_cache=False)

    installation_failed = False
    for font_type in ["Math", "Sans", "Roman"]:
        try:
            new_fontmanager.findfont(
                f"Latin Modern {font_type}", fallback_to_default=False
            )
        except ValueError:
            print(f"The font Latin Modern {font_type} was not found.")
            installation_failed = True

    if installation_failed:
        fail("At least one of the Latin Modern fonts was not installed correctly.")
