# Set style
# Deprecated since 3.11 function to access style file, to be updated
# https://docs.python.org/3/library/importlib.resources.html
import matplotlib.pyplot as plt
from importlib.resources import path as resources_path

def set_presentation_style():
    """
    Set the matplotlib style to a presentation-friendly style.
    Set by default when using plothist.

    Returns
    -------
    None
    """
    with resources_path("plothist", "presentation_style.mplstyle") as style_file:
        plt.style.use(style_file.as_posix())


def set_paper_style():
    """
    Set the matplotlib style to a paper-friendly (PRD) style.

    Returns
    -------
    None
    """
    with resources_path("plothist", "paper_style.mplstyle") as style_file:
        plt.style.use(style_file.as_posix())
