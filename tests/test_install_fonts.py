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
    # print matplotlib location
    import matplotlib
    try:
        print("matplotlib location ", matplotlib.__file__)
    except:
        print("matplotlib location ", "unknown")
    # print matplotlib font cache
    try:
        print("matplotlib font cache ", matplotlib.get_cachedir())
    except:
        print("matplotlib font cache ", "unknown")
    # print matplotlib font list
    try:
        print("matplotlib font list ", matplotlib.get_configdir())
    except:
        print("matplotlib font list ", "unknown")
    # print matplotlib font directory
    try:
        print("matplotlib font directory ", matplotlib.get_data_path())
    except:
        print("matplotlib font directory ", "unknown")

    install_latin_modern_fonts(font_directory=matplotlib.get_data_path()+"/fonts/ttf")

    for font_type in ["Math", "Sans", "Roman"]:
        try:
            findfont(f"Latin Modern {font_type}", fallback_to_default=False)
        except ValueError:
            fail(f"The font Latin Modern {font_type} was not found.")

    assert True