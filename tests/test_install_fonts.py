from plothist.scripts import install_latin_modern_fonts
from matplotlib.font_manager import findfont
from pytest import fail


def test_install_latin_modern_fonts():
    """
    Test install_latin_modern_fonts.
    """
    import plothist

    print("plothist folder ", plothist.__file__)

    from matplotlib.font_manager import findSystemFonts
    print(findSystemFonts(fontpaths=None, fontext="ttf"), " findSystemFonts")

    install_latin_modern_fonts()

    for font_type in ["Math", "Sans", "Roman"]:
        try:
            findfont(f"Latin Modern {font_type}", fallback_to_default=False)
        except ValueError:
            fail(f"The font {font_type} was not found.")

    assert True
