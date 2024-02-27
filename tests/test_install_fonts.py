# from plothist.scripts import install_latin_modern_fonts
from matplotlib.font_manager import findfont
import matplotlib
from pytest import fail

import subprocess
import os
import platform
from pathlib import PosixPath


def install_latin_modern_fonts(font_directory = None):
    """
    Install Latin Modern Math, Latin Modern Roman and Latin Modern Sans fonts.
    The font cache of matplotlib is removed, so matplotlib will be forced to update its font list.

    The Latin Modern Math font is available at http://mirrors.ctan.org/fonts/lm-math/opentype/latinmodern-math.otf
    The Latin Modern Roman and Latin Modern Sans fonts are available at https://www.1001fonts.com/latin-modern-roman-font.html and https://www.1001fonts.com/latin-modern-sans-font.html

    This function is only implemented for Linux and MacOS.

    Parameters:
    ----------
        font_directory: str, optional
            The directory where the fonts should be installed. If not given, the default directory is used.

    Raises:
    ------
        NotImplementedError: If the function is called on an unsupported operating system.
    """
    if platform.system() == "Linux":  # Linux
        font_directory = PosixPath("~/.fonts/").expanduser() if font_directory is None else PosixPath(font_directory).expanduser()
        font_directory.mkdir(parents=True, exist_ok=True)
        matplotlib_font_cache = PosixPath(
            "~/.cache/matplotlib/fontlist-v330.json"
        ).expanduser()
    elif platform.system() == "Darwin":  # MacOS
        font_directory = PosixPath(f"/Users/{os.getlogin()}/Library/Fonts").expanduser() if font_directory is None else PosixPath(font_directory).expanduser()
        matplotlib_font_cache = PosixPath(
            "~/.matplotlib/fontlist-v330.json"
        ).expanduser()
    else:
        raise NotImplementedError(
            f"This script is only implemented for Linux and MacOS. If you manage to make it work on {platform.system()}, please submit a pull request."
        )

    # Install Latin Modern Math
    subprocess.run(
        [
            "wget",
            "-P",
            font_directory,
            "http://mirrors.ctan.org/fonts/lm-math/opentype/latinmodern-math.otf",
        ]
    )
    # Install Latin Modern Roman and Latin Modern Sans
    for lm in ["roman", "sans"]:
        subprocess.run(
            [
                "wget",
                "-P",
                font_directory,
                f"https://www.1001fonts.com/download/latin-modern-{lm}.zip",
            ]
        )
        subprocess.run(
            [
                "unzip",
                "-o",
                (font_directory / f"latin-modern-{lm}.zip"),
                "-d",
                (font_directory / f"latin-modern-{lm}"),
            ]
        )
        subprocess.run(["rm", "-f", (font_directory / f"latin-modern-{lm}.zip")])

    # Remove font cache
    try:
        subprocess.run(
            ["rm", "-v", matplotlib_font_cache],
            check=True,
        )
    except subprocess.CalledProcessError:
        print(
            f"""
            Error while trying to remove {matplotlib_font_cache}, but maybe this is not needed.
            Check whether the Latin Modern fonts are now available in your matplotlib.
            If they are not, find the correct fontlist-XXX.json file in your matplotlib cache and remove it manually.
            """
        )


def test_install_latin_modern_fonts():
    """
    Test install_latin_modern_fonts.
    """

    from matplotlib.font_manager import findSystemFonts
    print("findSystemFonts")
    for elt in findSystemFonts(fontpaths=None, fontext="ttf"):
        print("> ",elt)
    try:
        print("findSystemFonts otf")
        for elt in findSystemFonts(fontpaths=None, fontext="otf"):
            print("> ",elt)
    except:
        pass

    print(findfont("DejaVuSerif", fallback_to_default=True))
    print(findfont("www", fallback_to_default=True))

    # print the current user plothist folder  /opt/hostedtoolcache/Python/3.8.18/x64/lib/python3.8/site-packages/plothist/__init__.py
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
    # ls in the matplotlib font directory
    try:
        print("ls in the matplotlib font directory ", os.listdir(matplotlib.get_data_path()+"/fonts/ttf/"))
    except:
        print("ls in the matplotlib font directory ", "unknown")

    failed = True
    for font_directory in [matplotlib.get_data_path()+"/fonts/ttf/", matplotlib.get_data_path()+"/fonts/", matplotlib.get_data_path(), None, "/usr/share/fonts/opentype/", "/usr/share/fonts/truetype/", "/usr/share/fonts/"]:
        install_latin_modern_fonts(font_directory=font_directory)
        matplotlib.font_manager._load_fontmanager(try_read_cache=False)
        print("\n")
        for font_type in ["Math", "Sans", "Roman"]:
            try:
                print(findfont(f"Latin Modern {font_type}", fallback_to_default=False))
                failed = False
                print(f"The font Latin Modern {font_type} was found with font_directory={font_directory}.")
            except ValueError:
                # failed = True
                print(f"The font Latin Modern {font_type} was not found.")
            try:
                print(findfont(f"Latin Modern {font_type}", fallback_to_default=False, fontext="otf"))
                failed = False
                print(f"The font Latin Modern {font_type} was found with font_directory={font_directory}.")
            except ValueError:
                # failed = True
                print(f"The font Latin Modern {font_type} was not found.")
            try:
                print(findfont(f"Latin Modern {font_type}", fallback_to_default=False, rebuild_if_missing=True))
                failed = False
                print(f"The font Latin Modern {font_type} was found with font_directory={font_directory}.")
            except ValueError:
                # failed = True
                print(f"The font Latin Modern {font_type} was not found.")


        # if failed:
        #     fail(f"Installation failed.")

    assert not failed
