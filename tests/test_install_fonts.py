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

    print(findfont("DejaVuSerif", fallback_to_default=True))
    print(findfont("www", fallback_to_default=True))

    # print the current user
    import os
    try:
        print("current user ", os.getlogin())
    except:
        print("current user ", "unknown")
    # print the current system
    import platform
    try:
        print("current platform ", platform.system())
    except:
        print("current platform ", "unknown")
    # print the current directory
    try:
        print("current directory ", os.getcwd())
    except:
        print("current directory ", "unknown")
    # print the current home directory
    try:
        print("current home directory ", os.path.expanduser("~"))
    except:
        print("current home directory ", "unknown")

    install_latin_modern_fonts(font_directory="/usr/share/fonts/truetype/")

    for font_type in ["Math", "Sans", "Roman"]:
        try:
            findfont(f"Latin Modern {font_type}", fallback_to_default=False)
        except ValueError:
            fail(f"The font Latin Modern {font_type} was not found.")

    assert True
