from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def set_style(style: str = "default") -> None:
    """
    Set the plothist style.

    Parameters
    ----------
    style : str, optional
        Switch between different styles. Default is 'default'. More style might come in the future.

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
    available_styles = ["default"]

    if style in available_styles:
        plt.style.use(f"plothist.{style}_style")
    else:
        raise ValueError(f"{style} not in the available styles: {available_styles}")


def cubehelix_palette(
    ncolors: int = 7,
    start: float = 1.5,
    rotation: float = 1.5,
    gamma: float = 1.0,
    hue: float = 0.8,
    lightest: float = 0.8,
    darkest: float = 0.3,
    reverse: bool = True,
) -> list[tuple[float, float, float]]:
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
    list[tuple[float, float, float]]
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
            # or high intensity values (gamma > 1)
            lambda_gamma = lambda_**gamma

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


def get_color_palette(
    cmap: str, N: int
) -> list[str] | list[tuple[float, float, float]]:
    """
    Get N different colors from a chosen colormap.

    Parameters
    ----------
    cmap : str
        The name of the colormap to use. Use "ggplot" get the cycle of the plothist style. Use "cubehelix" to get the cubehelix palette with default settings. Can also be any colormap from matplotlib (we recommend "viridis", "coolwarm" or "YlGnBu_r").
    N : int
        The number of colors to sample.

    Returns
    -------
    list[str] or list[tuple[float, float, float]]
        A list of colors. If "ggplot" is selected, returns a list of hex color strings.
        Otherwise, returns a list of RGB color tuples.

    References
    ----------
    ggplot colormap: https://matplotlib.org/stable/gallery/style_sheets/ggplot.html
    Matplotlib colormaps: https://matplotlib.org/stable/gallery/color/colormap_reference.html

    See also
    --------
    cubehelix_palette : Make a sequential palette from the cubehelix system.
    """
    if N < 1:
        raise ValueError("The number of colors asked should be >0.")

    if cmap == "ggplot":
        if N > 7:
            raise ValueError(
                f"Only 7 colors are available in the ggplot style cycle ({N} asked).",
            )
        return [
            "#348ABD",
            "#E24A33",
            "#988ED5",
            "#777777",
            "#FBC15E",
            "#8EBA42",
            "#FFB5B8",
        ][0:N]

    if cmap == "cubehelix":
        return cubehelix_palette(N)

    if N < 2:
        raise ValueError(
            "The number of colors asked should be >1 to sequence matplotlib palettes."
        )

    plt_cmap = plt.get_cmap(cmap)
    return plt_cmap(np.linspace(0, 1, N))


def set_fitting_ylabel_fontsize(ax: plt.Axes) -> float:
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

    # Force renderer to be initialized
    ax.figure.canvas.draw()

    while (
        ax.yaxis.get_label()
        .get_window_extent(renderer=ax.figure.canvas.get_renderer())
        .transformed(ax.transData.inverted())
        .y1
        > ax.get_ylim()[1]
    ):
        ylabel_fontsize -= 0.1

        if ylabel_fontsize <= 0:
            raise ValueError(
                "Only a y-label with a negative font size would fit on the y-axis."
            )

        ax.get_yaxis().get_label().set_size(ylabel_fontsize)

    return ylabel_fontsize


def add_text(
    text: str,
    x: float | str = "left",
    y: float | str = "top",
    fontsize: int = 12,
    white_background: bool = False,
    ax: plt.Axes | None = None,
    **kwargs,
) -> None:
    """
    Add text to an axis.

    Parameters
    ----------
    text : str
        The text to add.
    x : float | str, optional
        Horizontal position of the text in unit of the normalized x-axis length. The default is value "left", which is an alias for 0.0. Other aliases are "right", "left_in", "right_in", "right_out".
    y : float | str, optional
        Vertical position of the text in unit of the normalized y-axis length. The default is value "top", which is an alias for 1.01. Other aliases are "top_in", "bottom_in", "top_out"="top", "bottom_out"="bottom".
    fontsize : int, optional
        Font size, by default 12.
    white_background : bool, optional
        Draw a white rectangle under the text, by default False.
    ax : matplotlib.axes.Axes, optional
        Figure axis, by default None.
    kwargs : dict
        Keyword arguments to be passed to the ax.text() function.
        In particular, the keyword arguments ha and va, which are set by default to accommodate to the x and y aliases, can be used to change the text alignment.

    Raises
    ------
    ValueError
        If the x or y position is not a float or a valid position.

    Returns
    -------
    None
    """
    kwargs.setdefault("ha", "right" if x in ["right", "right_in"] else "left")
    kwargs.setdefault(
        "va", "top" if y in ["top_in", "bottom", "bottom_out"] else "bottom"
    )

    if ax is None:
        ax = plt.gca()
    transform = ax.transAxes

    x_values = {
        "left": 0.0,
        "right": 1.0,
        "left_in": 0.04,
        "right_in": 0.97,
        "right_out": 1.02,
    }

    y_values = {
        "top": 1.01,
        "bottom": -0.11,
        "top_out": 1.01,
        "bottom_out": -0.11,
        "top_in": 0.96,
        "bottom_in": 0.04,
    }

    if isinstance(x, str):
        if x not in x_values:
            raise ValueError(f"{x!r} is not a valid x position.")
        x = x_values[x]

    if isinstance(y, str):
        if y not in y_values:
            raise ValueError(f"{y!r} is not a valid y position.")
        y = y_values[y]

    t = ax.text(
        x,
        y,
        text,
        fontsize=fontsize,
        transform=transform,
        **kwargs,
    )

    # Add background
    if white_background:
        t.set_bbox({"facecolor": "white", "edgecolor": "white"})


def add_luminosity(
    collaboration: str,
    x: float | str = "right",
    y: float | str = "top",
    fontsize: int = 12,
    is_data: bool = True,
    lumi: int | str = "",
    lumi_unit: str = "fb",
    preliminary: bool = False,
    two_lines: bool = False,
    white_background: bool = False,
    ax: plt.Axes | None = None,
    **kwargs,
) -> None:
    """
    Add the collaboration name and the integrated luminosity (or "Simulation").

    Parameters
    ----------
    collaboration : str
        Collaboration name.
    x : float | str, optional
        Horizontal position of the text in unit of the normalized x-axis length. The default is value "right", which is an alias for 1.0. Can take other aliases such as "left", "left_in", "right_in", "right_out".
    y : float | str, optional
        Vertical position of the text in unit of the normalized y-axis length. The default is value "top", which is an alias for 1.01. Can take other aliases such as "top_in", "bottom_in", "top_out"="top", "bottom_out"="bottom".
    fontsize : int, optional
        Font size, by default 12.
    is_data : bool, optional
        If True, plot integrated luminosity. If False, plot "Simulation", by default True.
    lumi : int | str, optional
        Integrated luminosity. If empty, do not plot luminosity. Default value is empty.
    lumi_unit : str, optional
        Integrated luminosity unit. Default value is fb. The exponent is automatically -1.
    preliminary : bool, optional
        If True, print "preliminary", by default False.
    two_lines : bool, optional
        If True, write the information on two lines, by default False.
    white_background : bool, optional
        Draw a white rectangle under the text, by default False.
    ax : matplotlib.axes.Axes, optional
        Figure axis, by default None.
    kwargs : dict
        Keyword arguments to be passed to the ax.text() function.
        In particular, the keyword arguments ha and va, which are set to "left" (or "right" if x="right") and "bottom" by default, can be used to change the text alignment.

    Returns
    -------
    None

    See Also
    --------
    add_text : Add information on the plot.
    """

    text = (
        r"$\mathrm{\mathbf{"
        + collaboration.replace(" ", r"\,\,")
        + "}"
        + (r"\,\,preliminary}$" if preliminary else "}$")
    )
    if two_lines:
        text += "\n"
    else:
        text += " "
    if is_data:
        if lumi:
            text += rf"$\int\,\mathcal{{L}}\,\mathrm{{d}}\mathit{{t}}={lumi}\,{lumi_unit}^{{-1}}$"
    else:
        text += r"$\mathrm{simulation}$"

    add_text(
        text,
        x,
        y,
        fontsize=fontsize,
        white_background=white_background,
        ax=ax,
        **kwargs,
    )


def plot_reordered_legend(ax: plt.Axes, order: list[int], **kwargs) -> None:
    """
    Reorder the legend handlers and labels on the given Matplotlib axis based
    on the specified order and plot the reordered legend.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Matplotlib Axes object on which the legend is to be reordered.
    order : list[int]
        A list of integers specifying the new order of the legend items.
        The integers refer to the indices of the current legend items.
    kwargs : dict, optional
        Keyword arguments to be passed to the ax.legend() function, such as the legend location (loc).

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the order list does not contain all integers from 0 to
        len(labels) - 1.

    Examples
    --------

    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], label='Line 1')
    >>> ax.plot([3, 2, 1], label='Line 2')

    To reorder the legend so that 'Line 2' comes first, use:

    >>> plot_reordered_legend(ax, [1, 0])
    """

    # Extract the original handlers and labels
    handlers, labels = ax.get_legend_handles_labels()

    # Check if order is valid
    if not all(i in range(len(labels)) for i in order) or len(set(order)) < len(order):
        raise ValueError(
            f"The order list should contain all integers from 0 to {len(labels) - 1}."
        )

    # Reorder handlers and labels
    new_handlers = [handlers[i] for i in order]
    new_labels = [labels[i] for i in order]

    # Draw the new legend
    ax.legend(new_handlers, new_labels, **kwargs)
