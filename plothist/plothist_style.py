# Set style
# Deprecated since 3.11 function to access style file, to be updated
# https://docs.python.org/3/library/importlib.resources.html
import matplotlib.pyplot as plt
from importlib.resources import path as resources_path


def set_style(style="presentation"):
    """
    Set the matplotlib style.

    Parameters
    ----------
    style : str, optional
        Switch between different styles. Default is 'presentation'.
        Available styles: ['presentation', 'publication']

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the specified style is not in the available styles.

    Notes
    -----
    - The 'presentation' style is set by default when using plothist.
    """
    available_styles = ["presentation", "publication"]

    if style in available_styles:
        with resources_path("plothist", f"{style}_style.mplstyle") as style_file:
            plt.style.use(style_file.as_posix())
    else:
        raise ValueError(f"{style} not in the available styles: {available_styles}")
