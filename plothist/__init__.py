"""Plot histograms in a scalable way and a beautiful style."""
__version__ = "0.8.1"

from .plotters import (
    create_comparison_figure,
    create_axis,
    make_hist,
    make_2d_hist,
    plot_hist,
    plot_2d_hist,
    plot_2d_hist_with_projections,
    plot_error_hist,
    compare_two_hist,
    plot_comparison,
)

from .variable_registry import (
    create_variable_registry,
    get_variable_from_registry,
    update_variable_registry_ranges,
)

from .hep_plotters import compare_data_mc, plot_mc, add_luminosity

from .plothist_style import (
    set_style,
    cubehelix_palette,
    get_color_palette,
    set_fitting_ylabel_fontsize,
    add_text,
)

__all__ = [
    "__version__",
    "create_variable_registry",
    "get_variable_from_registry",
    "update_variable_registry_ranges",
    "create_comparison_figure",
    "create_axis",
    "make_hist",
    "make_2d_hist",
    "plot_hist",
    "plot_2d_hist",
    "plot_2d_hist_with_projections",
    "plot_error_hist",
    "compare_two_hist",
    "plot_comparison",
    "compare_data_mc",
    "plot_mc",
    "add_luminosity",
    "set_style",
    "cubehelix_palette",
    "get_color_palette",
    "set_fitting_ylabel_fontsize",
    "add_text",
]


# Get style file and use it
# Deprecated since 3.11 function to access style file, to be updated
# https://docs.python.org/3/library/importlib.resources.html
import matplotlib.pyplot as plt
from importlib.resources import path as resources_path

with resources_path("plothist", "default_style.mplstyle") as style_file:
    plt.style.use(style_file.as_posix())

# Check the fonts
from matplotlib.font_manager import findfont
import warnings

for font_type in ["Math", "Sans", "Roman"]:
    try:
        findfont(f"Latin Modern {font_type}", fallback_to_default=False)
    except:
        warnings.warn(
            "The recommended fonts to use plothist were not found. You can install them by typing 'install_latin_modern_fonts' in your terminal. \n",
            stacklevel=3,
        )
        break
