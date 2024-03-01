import subprocess
import os
import platform
from pathlib import PosixPath
import time


def _get_install_command(url, font_directory):
    """
    Get the command to install a font.

    Parameters
    ----------
    url : str
        The URL of the font.
    font_directory : PosixPath
        The directory where the font should be installed.

    Returns
    -------
    list
        The command to run in a subprocess to install the font.
    """
    return [
        "wget",
        "--retry-connrefused",  # retry refused connections and similar fatal errors
        "--retry-on-host-error",  # retry on host errors such as 404 "Not Found"
        "--waitretry=1",  # wait 1 second before next retry
        "--read-timeout=20",  # wait a maximum of 20 seconds in case no data is received and then try again
        "--timeout=15",  # wait max 15 seconds before the initial connection times out
        "-t",
        "10",  # retry 10 times
        "-P",
        font_directory,
        url,
    ]


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
        matplotlib_font_cache = PosixPath(
            "~/.cache/matplotlib/fontlist-v330.json"
        ).expanduser()
    elif platform.system() == "Darwin":  # MacOS
        font_directory = PosixPath(f"/Users/{os.getlogin()}/Library/Fonts").expanduser()
        matplotlib_font_cache = PosixPath(
            "~/.matplotlib/fontlist-v330.json"
        ).expanduser()
    else:
        raise NotImplementedError(
            f"This script is only implemented for Linux and MacOS. If you manage to make it work on {platform.system()}, please submit a pull request."
        )

    # Install Latin Modern Math
    print("Downloading Latin Modern Math...")
    attempt = 0
    max_attempt = 10
    success = False

    while not success and attempt < max_attempt:
        result = subprocess.run(
            _get_install_command(
                "http://mirrors.ctan.org/fonts/lm-math/opentype/latinmodern-math.otf",
                font_directory,
            ),
            capture_output=True,
            text=True,
        )
        success = result.returncode == 0
        if not success:
            # Print the output to the terminal
            print("Try", attempt + 1, "of", max_attempt)
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            # Increment attempt counter and wait before the next attempt
            attempt += 1
            time.sleep(5)

    if not success:
        raise RuntimeError(
            f"Failed to download Latin Modern Math after {max_attempt} attempts. Try to install it manually (see https://plothist.readthedocs.io/en/latest/usage/font_installation.html)."
        )
    print("Latin Modern Math downloaded successfully.\n")

    # Install Latin Modern Roman and Latin Modern Sans
    for lm in ["roman", "sans"]:
        print(f"Downloading Latin Modern {lm}...")

        attempt = 0
        max_attempt = 10
        success = False

        while not success and attempt < max_attempt:
            result = subprocess.run(
                _get_install_command(
                    f"https://www.1001fonts.com/download/latin-modern-{lm}.zip",
                    font_directory,
                ),
                capture_output=True,
                text=True,
            )
            success = result.returncode == 0
            if not success:
                # Print the output to the terminal
                print("Try", attempt + 1, "of", max_attempt)
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                # Increment attempt counter and wait before the next attempt
                attempt += 1
                time.sleep(5)

        if not success:
            raise RuntimeError(
                f"Failed to download Latin Modern {lm} after {max_attempt} attempts. Try to install it manually (see https://plothist.readthedocs.io/en/latest/usage/font_installation.html)."
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

        print(f"Latin Modern {lm} downloaded successfully.\n")

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
            If it still does not work, please check the documentation at https://plothist.readthedocs.io/en/latest/usage/font_installation.html.
            """
        )


if __name__ == "__main__":
    install_latin_modern_fonts()
