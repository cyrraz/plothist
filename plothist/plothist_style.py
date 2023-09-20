# Set style
# Deprecated since 3.11 function to access style file, to be updated
# https://docs.python.org/3/library/importlib.resources.html
import matplotlib.pyplot as plt
from importlib.resources import path as resources_path


def set_style(style="default"):
    """
    Set the matplotlib style.

    Parameters
    ----------
    style : str, optional
        Switch between different styles. Default is 'default'.
        Available styles: ['default', 'small']

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the specified style is not in the available styles.

    Notes
    -----
    - The default plothist style is tuned to be presentation and publication ready.
    """
    available_styles = ["default", "small"]

    if style in available_styles:
        with resources_path("plothist", f"{style}_style.mplstyle") as style_file:
            plt.style.use(style_file.as_posix())
    else:
        raise ValueError(f"{style} not in the available styles: {available_styles}")


def get_fitting_ylabel_fontsize(ax):
    """
    Get the suitable font size for a ylabel text that fits within the plot's y-axis limits.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib subplot to adjust the ylabel font size for.

    Returns
    -------
    float
        The adjusted font size for the ylabel text.
    """
    ylabel_fontsize = ax.yaxis.get_label().get_fontsize()
    while (
        ax.yaxis.get_label().get_window_extent().transformed(ax.transData.inverted()).y1
        > ax.get_ylim()[1]
    ):
        ylabel_fontsize -= 0.1
        ax.get_yaxis().get_label().set_size(ylabel_fontsize)
        if ylabel_fontsize < 0:
            raise ValueError(
                "Only a y-label with a negative font size would fit on the y-axis."
            )
    return ylabel_fontsize
