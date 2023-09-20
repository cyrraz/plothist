# Set style
# Deprecated since 3.11 function to access style file, to be updated
# https://docs.python.org/3/library/importlib.resources.html
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
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


def cubehelix_palette(
    ncolors=7,
    start=1.5,
    rotation=1.5,
    gamma=1.0,
    hue=0.8,
    lightest=0.8,
    darkest=0.3,
    reverse=True,
):
    """
    Make a sequential palette from the cubehelix system, in which the perceived brightness is linearly increasing.
    This code is adapted from seaborn, which implements equation (2) of reference [1] below.

    Parameters
    ----------
    ncolors : int, optional
        Number of colors in the palette.
    start : float, 0 <= start <= 3, optional
        Direction of the predominant colour deviation from black
        at the start of the colour scheme (1=red, 2=green, 3=blue).
    rotation : float, optional
        Number of rotations around the hue wheel over the range of the palette.
    gamma : float, 0 <= gamma, optional
        Gamma factor to emphasize darker (gamma < 1) or lighter (gamma > 1)
        colors.
    hue : float, 0 <= hue <= 1, optional
        Saturation of the colors.
    darkest : float, 0 <= darkest <= 1, optional
        Intensity of the darkest color in the palette.
    lightest : float, 0 <= lightest <= 1, optional
        Intensity of the lightest color in the palette.
    reverse : bool, optional
        If True, the palette will go from dark to light.

    Returns
    -------
    list of RGB tuples
        The generated palette of colors represented as a list of RGB tuples.


    References
    ----------
    [1] Green, D. A. (2011). "A colour scheme for the display of astronomical
    intensity images". Bulletin of the Astromical Society of India, Vol. 39,
    p. 289-295.
    """

    def f(x0, x1):
        # Adapted from matplotlib
        def color(lambda_):
            # emphasise either low intensity values (gamma < 1),
            # or high intensity values (γ > 1)
            lambda_gamma = lambda_ ** gamma

            # Angle and amplitude for the deviation
            # from the black to white diagonal
            # in the plane of constant perceived intensity
            a = hue * lambda_gamma * (1 - lambda_gamma) / 2

            phi = 2 * np.pi * (start / 3 + rotation * lambda_)

            return lambda_gamma + a * (x0 * np.cos(phi) + x1 * np.sin(phi))

        return color

    cdict = {
        "red": f(-0.14861, 1.78277),
        "green": f(-0.29227, -0.90649),
        "blue": f(1.97294, 0.0),
    }

    cmap = mpl.colors.LinearSegmentedColormap("cubehelix", cdict)

    x = np.linspace(lightest, darkest, int(ncolors))
    pal = cmap(x)[:, :3].tolist()
    if reverse:
        pal = pal[::-1]
    return pal


def get_cmap_palette(cmap, N):
    """
    Get N different colors from a specified colormap from matplotlib.

    Parameters
    ----------
    cmap : str
        The name of the colormap to use.
    N : int
        The number of colors to sample.

    Returns
    -------
    list
        A list of RGB color tuples sampled from the colormap, reversed.

    References
    ----------
    Matplotlib colormaps: https://matplotlib.org/stable/gallery/color/colormap_reference.html
    """
    plt_cmap = plt.get_cmap(cmap)

    values = np.linspace(0, 1, N)

    colors = [plt_cmap(value) for value in values]

    return colors[::-1]


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

        if ylabel_fontsize <= 0:
            raise ValueError(
                "Only a y-label with a negative font size would fit on the y-axis."
            )

        ax.get_yaxis().get_label().set_size(ylabel_fontsize)

    return ylabel_fontsize
