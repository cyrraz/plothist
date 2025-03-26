import os
import platform
import subprocess
import time
from pathlib import PosixPath
from zipfile import ZipFile

import matplotlib
import requests


def _download_font(url, font_directory, font_name):
    """
    Download a font from a URL and save it in a directory.

    Parameters
    ----------
    url : str
        The URL of the font.
    font_directory : PosixPath
        The directory where the font should be installed.

    Raises
    ------
    RuntimeError
        If the download fails.
    """
    print(f"Downloading {font_name}...")
    attempt = 0
    max_attempt = 10
    success = False

    while not success and attempt < max_attempt:
        try:
            r = requests.get(url)
            with (font_directory / url.split("/")[-1]).open("wb") as f:
                f.write(r.content)
            success = True
        except Exception as e:
            # Print the output to the terminal
            print(f"Error: {e}\nTry {attempt + 1} of {max_attempt}")
            # Increment attempt counter and wait before the next attempt
            attempt += 1
            time.sleep(attempt)

    if not success:
        raise RuntimeError(
            f"Failed to download {font_name} after {max_attempt} attempts. Try to install it manually (see https://plothist.readthedocs.io/en/latest/usage/font_installation.html)."
        )
    print(f"{font_name} downloaded successfully.")


def install_latin_modern_fonts():
    """
    Install Latin Modern Math, Latin Modern Roman and Latin Modern Sans fonts.
    The font cache of matplotlib is removed, so matplotlib will be forced to update its font list.

    The Latin Modern Math font is available at http://mirrors.ctan.org/fonts/lm-math/opentype/latinmodern-math.otf
    The Latin Modern Roman and Latin Modern Sans fonts are available at https://www.1001fonts.com/latin-modern-roman-font.html and https://www.1001fonts.com/latin-modern-sans-font.html

    This function is only implemented for Linux and MacOS.

    Raises:
    ------
        NotImplementedError: If the function is called on an unsupported operating system.
        RuntimeError: If the installation of the fonts fails.
    """
    if platform.system() == "Linux":  # Linux
        font_directory = PosixPath("~/.fonts/").expanduser()
        font_directory.mkdir(parents=True, exist_ok=True)
    elif platform.system() == "Darwin":  # MacOS
        font_directory = PosixPath(f"/Users/{os.getlogin()}/Library/Fonts").expanduser()
    else:
        raise NotImplementedError(
            f"This script is only implemented for Linux and MacOS. If you manage to make it work on {platform.system()}, please submit a pull request."
        )

    if not PosixPath(font_directory / "latinmodern-math.otf").exists():
        # Install Latin Modern Math
        _download_font(
            "http://mirrors.ctan.org/fonts/lm-math/opentype/latinmodern-math.otf",
            font_directory,
            "Latin Modern Math",
        )
        print("Latin Modern Math installed successfully.\n")
    else:
        print("Latin Modern Math already installed.\n")

    # Install Latin Modern Roman and Latin Modern Sans
    for lm in ["roman", "sans"]:
        if PosixPath(font_directory / f"latin-modern-{lm}").exists():
            print(f"Latin Modern {lm} already installed.\n")
            continue

        attempt = 0
        max_attempt = 10
        success = False

        while not success and attempt < max_attempt:
            _download_font(
                f"https://www.1001fonts.com/download/latin-modern-{lm}.zip",
                font_directory,
                f"Latin Modern {lm}",
            )
            print(f"Unzipping Latin Modern {lm}...")

            try:
                with ZipFile(font_directory / f"latin-modern-{lm}.zip", "r") as zip_ref:
                    zip_ref.extractall(font_directory / f"latin-modern-{lm}")
                    success = True
            except Exception as e:
                # Print the output to the terminal
                print(f"Error: {e}\nTry {attempt + 1} of {max_attempt}")
                # Increment attempt counter and wait before the next attempt
                attempt += 1
                time.sleep(attempt)
                subprocess.run(
                    ["rm", "-f", (font_directory / f"latin-modern-{lm}.zip")]
                )

        print(f"Latin Modern {lm} installed successfully.\n")
        subprocess.run(["rm", "-f", (font_directory / f"latin-modern-{lm}.zip")])

    # Remove font cache files
    matplotlib_font_cache_files = PosixPath(matplotlib.get_cachedir()).glob(
        "fontlist-v???.json"
    )
    for matplotlib_font_cache in matplotlib_font_cache_files:
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
                If it still does not work, please check the documentation at https://plothist.readthedocs.io/en/latest/usage/font_installation.html
                """
            )


if __name__ == "__main__":
    install_latin_modern_fonts()
