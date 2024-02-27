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
    # try:
    #     subprocess.run(
    #         ["rm", "-v", matplotlib_font_cache],
    #         check=True,
    #     )
    # except subprocess.CalledProcessError:
    #     print(
    #         f"""
    #         Error while trying to remove {matplotlib_font_cache}, but maybe this is not needed.
    #         Check whether the Latin Modern fonts are now available in your matplotlib.
    #         If they are not, find the correct fontlist-XXX.json file in your matplotlib cache and remove it manually.
    #         """
    #     )


if __name__ == "__main__":
    install_latin_modern_fonts()
