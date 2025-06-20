import matplotlib.pyplot as plt
import pytest

from plothist import (
    add_luminosity,
    add_text,
    get_color_palette,
    plot_reordered_legend,
    set_fitting_ylabel_fontsize,
    set_style,
)


def test_set_style_invalid_value() -> None:
    """
    Test that set_style raises a ValueError when an unsupported style is passed.
    """
    # pytest.raises checks that a ValueError is raised and its message matches the expected string
    with pytest.raises(
        ValueError, match="nonexistent not in the available styles: \\['default'\\]"
    ):
        set_style("nonexistent")


def test_get_color_palette_raises() -> None:
    """
    Test that get_color_palette raises ValueError for:
    - N < 1 (general case)
    - N > 7 when cmap is 'ggplot'
    - N < 2 when cmap is any matplotlib colormap (excluding 'ggplot' and 'cubehelix')
    """
    with pytest.raises(ValueError, match="The number of colors asked should be >0."):
        get_color_palette("viridis", 0)

    with pytest.raises(
        ValueError, match="Only 7 colors are available in the ggplot style cycle"
    ):
        get_color_palette("ggplot", 8)

    with pytest.raises(
        ValueError,
        match="The number of colors asked should be >1 to sequence matplotlib palettes.",
    ):
        get_color_palette("viridis", 1)


def test_set_fitting_ylabel_fontsize_raises() -> None:
    """
    Test that set_fitting_ylabel_fontsize raises a ValueError when the y-label cannot fit even at the smallest font size.
    """
    fig, ax = plt.subplots(figsize=(0.1, 0.1))
    ax.set_ylabel("Test Y-Label", fontsize=1)

    with pytest.raises(
        ValueError,
        match="Only a y-label with a negative font size would fit on the y-axis.",
    ):
        set_fitting_ylabel_fontsize(ax)

    plt.close(fig)


def test_add_text_invalid_positions() -> None:
    """
    Test that add_text raises ValueError for invalid x and y string positions.
    """
    fig, ax = plt.subplots()

    with pytest.raises(ValueError, match="'invalid_x' is not a valid x position."):
        add_text("Test", x="invalid_x", ax=ax)

    with pytest.raises(ValueError, match="'invalid_y' is not a valid y position."):
        add_text("Test", y="invalid_y", ax=ax)

    plt.close(fig)


def test_add_text_white_background():
    """
    Test that add_text sets a white background box around the text when white_background is True.
    """
    fig, ax = plt.subplots()
    add_text("Test", white_background=True, ax=ax)

    # Assert that the text has a white background box set
    text_obj = ax.texts[0]
    bbox = text_obj.get_bbox_patch()
    assert bbox.get_facecolor()[:3] == (1.0, 1.0, 1.0)

    plt.close(fig)


def test_add_luminosity_two_lines():
    """
    Test that add_luminosity produces a two-line label when two_lines is True.
    """
    fig, ax = plt.subplots()
    add_luminosity("Test Collaboration", two_lines=True, ax=ax)

    assert "\n" in ax.texts[0].get_text()

    plt.close(fig)


def test_plot_reordered_legend_valid_and_invalid():
    """
    Test that plot_reordered_legend works correctly with a valid order
    and raises ValueError with an invalid order.
    """
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], label="A")
    ax.plot([3, 2, 1], label="B")
    ax.legend()

    # Valid call: reorder legend to [B, A]
    plot_reordered_legend(ax, [1, 0])  # Should not raise

    # Invalid call: duplicate and missing index
    with pytest.raises(
        ValueError, match="The order list should contain all integers from 0 to 1."
    ):
        plot_reordered_legend(ax, [0, 0])

    plt.close(fig)
