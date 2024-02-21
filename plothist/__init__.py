"""Plot histograms in a scalable way and a beautiful style."""

__version__ = "1.0.6"

from .plotters import (
    create_comparison_figure,
    plot_hist,
    plot_2d_hist,
    plot_2d_hist_with_projections,
    plot_error_hist,
    plot_hist_uncertainties,
    plot_two_hist_comparison,
    plot_comparison,
    savefig,
    plot_data_model_comparison,
    plot_model,
    plot_function,
)

from .histogramming import (
    create_axis,
    make_hist,
    make_2d_hist,
    flatten_2d_hist,
)

from .variable_registry import (
    create_variable_registry,
    get_variable_from_registry,
    update_variable_registry,
    remove_variable_registry_parameters,
    update_variable_registry_ranges,
)

from .comparison import (
    get_asymmetrical_uncertainties,
    get_comparison,
    get_pull,
    get_difference,
    get_ratio,
    get_ratio_variances,
)

from .plothist_style import (
    set_style,
    cubehelix_palette,
    get_color_palette,
    set_fitting_ylabel_fontsize,
    add_text,
    add_luminosity,
    plot_reordered_legend,
)

from .get_dummy_data import get_dummy_data

__all__ = [
    "__version__",
    "create_variable_registry",
    "get_variable_from_registry",
    "update_variable_registry",
    "remove_variable_registry_parameters",
    "update_variable_registry_ranges",
    "create_comparison_figure",
    "create_axis",
    "make_hist",
    "make_2d_hist",
    "plot_hist",
    "plot_2d_hist",
    "plot_2d_hist_with_projections",
    "plot_error_hist",
    "plot_hist_uncertainties",
    "plot_two_hist_comparison",
    "plot_comparison",
    "savefig",
    "plot_data_model_comparison",
    "plot_model",
    "plot_function",
    "add_luminosity",
    "get_asymmetrical_uncertainties",
    "set_style",
    "cubehelix_palette",
    "get_color_palette",
    "set_fitting_ylabel_fontsize",
    "add_text",
    "get_asymmetrical_uncertainties",
    "get_comparison",
    "get_pull",
    "get_difference",
    "get_ratio",
    "get_ratio_variances",
    "flatten_2d_hist",
    "plot_reordered_legend",
    "get_dummy_data",
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
