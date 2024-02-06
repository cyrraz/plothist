import subprocess
import os
import platform
from pathlib import Path


def install_latin_modern_fonts():
    """
    Install Latin Modern fonts for matplotlib and clean the font cache.
    """
    if platform.system() == "Linux":  # Linux
        font_directory = Path(os.path.expanduser("~/.fonts/"))
        font_directory.mkdir(parents=True, exist_ok=True)
        matplotlib_font_cache = Path(
            os.path.expanduser("~/.cache/matplotlib/fontlist-v330.json")
        )
    if platform.system() == "Darwin":  # MacOS
        font_directory = Path(f"/Users/{os.getlogin()}/Library/Fonts")
        matplotlib_font_cache = Path(
            os.path.expanduser("~/.matplotlib/fontlist-v330.json")
        )

    # Install Latin Modern Math
    subprocess.run(
        [
            "wget",
            "-P",
            font_directory.as_posix(),
            "http://mirrors.ctan.org/fonts/lm-math/opentype/latinmodern-math.otf",
        ]
    )
    # Install Latin Modern Roman and Latin Modern Sans
    for lm in ["roman", "sans"]:
        subprocess.run(
            [
                "wget",
                "-P",
                font_directory.as_posix(),
                f"https://www.1001fonts.com/download/latin-modern-{lm}.zip",
            ]
        )
        subprocess.run(
            [
                "unzip",
                "-o",
                (font_directory / f"latin-modern-{lm}.zip").as_posix(),
                "-d",
                (font_directory / f"latin-modern-{lm}").as_posix(),
            ]
        )
        subprocess.run(
            ["rm", "-f", (font_directory / f"latin-modern-{lm}.zip").as_posix()]
        )

    # Remove font cache
    try:
        subprocess.run(
            ["rm", "-v", matplotlib_font_cache.as_posix()],
            check=True,
        )
    except subprocess.CalledProcessError:
        print(
            f"""
            Error while trying to remove {matplotlib_font_cache.as_posix()}, but maybe this is not needed.
            Check whether the Latin Modern fonts are now available in your matplotlib.
            If they are not, find the correct fontlist-XXX.json file in your matplotlib cache and remove it manually.
            """
        )


if __name__ == "__main__":
    install_latin_modern_fonts()
