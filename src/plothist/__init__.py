"""Plot histograms in a scalable way and a beautiful style."""

__version__ = "1.3.0"

from .comparison import (
    get_asymmetrical_uncertainties,
    get_comparison,
    get_difference,
    get_pull,
    get_ratio,
    get_ratio_variances,
)
from .get_dummy_data import get_dummy_data
from .histogramming import (
    flatten_2d_hist,
    make_2d_hist,
    make_hist,
)
from .plothist_style import (
    add_luminosity,
    add_text,
    cubehelix_palette,
    get_color_palette,
    plot_reordered_legend,
    set_fitting_ylabel_fontsize,
    set_style,
)
from .plotters import (
    create_comparison_figure,
    plot_2d_hist,
    plot_2d_hist_with_projections,
    plot_comparison,
    plot_data_model_comparison,
    plot_error_hist,
    plot_function,
    plot_hist,
    plot_hist_uncertainties,
    plot_model,
    plot_two_hist_comparison,
    savefig,
)
from .variable_registry import (
    create_variable_registry,
    get_variable_from_registry,
    remove_variable_registry_parameters,
    update_variable_registry,
    update_variable_registry_ranges,
)

__all__ = [
    "__version__",
    "add_luminosity",
    "add_text",
    "create_comparison_figure",
    "create_variable_registry",
    "cubehelix_palette",
    "flatten_2d_hist",
    "get_asymmetrical_uncertainties",
    "get_asymmetrical_uncertainties",
    "get_color_palette",
    "get_comparison",
    "get_difference",
    "get_dummy_data",
    "get_pull",
    "get_ratio",
    "get_ratio_variances",
    "get_variable_from_registry",
    "make_2d_hist",
    "make_hist",
    "plot_2d_hist",
    "plot_2d_hist_with_projections",
    "plot_comparison",
    "plot_data_model_comparison",
    "plot_error_hist",
    "plot_function",
    "plot_hist",
    "plot_hist_uncertainties",
    "plot_model",
    "plot_reordered_legend",
    "plot_two_hist_comparison",
    "remove_variable_registry_parameters",
    "savefig",
    "set_fitting_ylabel_fontsize",
    "set_style",
    "update_variable_registry",
    "update_variable_registry_ranges",
]


# Get style file and use it
# Deprecated since 3.11 function to access style file, to be updated
# https://docs.python.org/3/library/importlib.resources.html
from importlib.resources import path as resources_path

import matplotlib.pyplot as plt

with resources_path("plothist", "default_style.mplstyle") as style_file:
    plt.style.use(style_file.as_posix())

# Check the fonts
import warnings

from matplotlib.font_manager import findfont

for font_type in ["Math", "Sans", "Roman"]:
    try:
        findfont(f"Latin Modern {font_type}", fallback_to_default=False)
    except:
        warnings.warn(
            "The recommended fonts to use plothist were not found. You can install them by typing 'install_latin_modern_fonts' in your terminal. If it still does not work, please check the documentation at https://plothist.readthedocs.io/en/latest/usage/font_installation.html",
            stacklevel=3,
        )
        break
