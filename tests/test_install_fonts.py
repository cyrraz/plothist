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
    print("findSystemFonts")
    for elt in findSystemFonts(fontpaths=None, fontext="ttf"):
        print("> ",elt)

    print("\nTry to find Lato-HairlineItalic")
    print(findfont(f"Lato-HairlineItalic", fallback_to_default=False))

    install_latin_modern_fonts(font_directory="/usr/share/fonts/truetype/")

    for font_type in ["Math", "Sans", "Roman"]:
        try:
            findfont(f"Latin Modern {font_type}", fallback_to_default=False)
        except ValueError:
            fail(f"The font {font_type} was not found.")

    assert True
